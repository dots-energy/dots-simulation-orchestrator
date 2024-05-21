#  This work is based on original code developed and copyrighted by TNO 2023.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO

from datetime import datetime, timedelta
import typing
import time

import kubernetes.client

from simulation_orchestrator.model_services_orchestrator.constants import SIMULATION_NAMESPACE
from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.model_services_orchestrator.types import ModelState
from simulation_orchestrator.models.model_inventory import Model
from simulation_orchestrator.types import ModelId, SimulationId, SimulatorId
import json

HELICS_BROKER_POD_NAME = 'helics-broker'
HELICS_BROKER_IMAGE_URL = 'dotsenergyframework/helics-broker:0.0.1'
HELICS_BROKER_PORT = 30000

class PodStatus:
    simulator_id: SimulatorId
    model_id: ModelId
    model_state: ModelState
    exit_code: typing.Optional[int]
    exit_reason: typing.Optional[str]
    delete_by: typing.Optional[datetime]

    def __init__(self,  # pylint: disable=too-many-arguments
                 simulator_id: SimulatorId,
                 model_id: ModelId,
                 model_state: ModelState,
                 exit_code: typing.Optional[int],
                 exit_reason: typing.Optional[str],
                 delete_by: typing.Optional[datetime]):
        self.simulator_id = simulator_id
        self.model_id = model_id
        self.model_state = model_state
        self.exit_code = exit_code
        self.exit_reason = exit_reason
        self.delete_by = delete_by


class K8sApi:
    k8s_core_api: kubernetes.client.CoreV1Api
    k8s_apps_api: kubernetes.client.AppsV1Api
    pull_image_secret_name: str

    def __init__(self,
                 kubernetes_client: kubernetes.client.ApiClient,
                 pull_image_secret_name: str,
                 generic_model_env_var:dict):
        self.k8s_core_api = kubernetes.client.CoreV1Api(kubernetes_client)
        self.k8s_apps_api = kubernetes.client.AppsV1Api(kubernetes_client)
        self.pull_image_secret_name = pull_image_secret_name
        self.generic_model_env_var = generic_model_env_var

    def deploy_new_pod(self, pod_name, container_url, env_vars, labels):
        LOGGER.info(f'Deploying pod {pod_name}')
        k8s_container = kubernetes.client.V1Container(image=container_url,
                                                      env=env_vars,
                                                      name=pod_name,
                                                      image_pull_policy='IfNotPresent')
        if self.pull_image_secret_name:
            LOGGER.debug(f'Using pull image secret name {self.pull_image_secret_name}')
            image_pull_secrets = [kubernetes.client.V1LocalObjectReference(name=self.pull_image_secret_name)]
        else:
            LOGGER.debug('Not using pull image secret name.')
            image_pull_secrets = []
        k8s_pod_spec = kubernetes.client.V1PodSpec(restart_policy='Never',
                                                   containers=[k8s_container],
                                                   node_selector={
                                                       'type': 'worker'
                                                   },
                                                   image_pull_secrets=image_pull_secrets)

        k8s_pod_metadata = kubernetes.client.V1ObjectMeta(name=pod_name,
                                                          labels=labels)
        k8s_pod = kubernetes.client.V1Pod(spec=k8s_pod_spec,
                                          metadata=k8s_pod_metadata,
                                          kind='Pod',
                                          api_version='v1')

        try:
            self.k8s_core_api.create_namespaced_pod(namespace=SIMULATION_NAMESPACE, body=k8s_pod)
            succeeded = True
        except kubernetes.client.ApiException as exc:
            LOGGER.warning(f'Could not create model {pod_name}. '
                           f'Reason: {exc.reason} ({exc.status}), {exc.body}')
            succeeded = False

        return succeeded
    
    def await_pod_to_running_state(self, pod_name):
        broker_ip = None
        LOGGER.info("Waiting for broker to be in running state")
        while broker_ip == None:
            api_response = self.k8s_core_api.list_namespaced_pod(SIMULATION_NAMESPACE, field_selector=f'metadata.name={pod_name}')
            for pod in api_response.items:
                if pod.status.container_statuses:
                    container_k8s_status = pod.status.container_statuses[0].state
                    if container_k8s_status.running:
                        broker_ip = pod.status.pod_ip
            time.sleep(1)
        return broker_ip

    def deploy_helics_broker(self, amount_of_federates, simulation_id, simulator_id):
        broker_pod_name = f'{HELICS_BROKER_POD_NAME}-{simulation_id}'
        self.deploy_new_pod(broker_pod_name, HELICS_BROKER_IMAGE_URL,[kubernetes.client.V1EnvVar("AMOUNT_OF_FEDERATES", str(amount_of_federates)), kubernetes.client.V1EnvVar("HELICS_BROKER_PORT", str(HELICS_BROKER_PORT))], {'simulation_id': simulation_id, 'simulator_id': simulator_id, 'model_id': broker_pod_name})
        broker_ip = self.await_pod_to_running_state(broker_pod_name)
        return broker_ip

    def deploy_model(self, simulator_id: SimulatorId, simulation_id: SimulationId, model: Model,
                           keep_logs_hours: float) -> bool:
        pod_name = self.model_to_pod_name(simulator_id, simulation_id, model.model_id)
        LOGGER.info(f'Deploying pod {pod_name}')
        labels={
            'simulator_id': simulator_id,
            'simulation_id': simulation_id,
            'model_id': model.model_id,
            'keep_logs_hours': str(keep_logs_hours),
        }
        env_vars = self.generic_model_env_var
        env_vars["esdl_ids"] = ';'.join(model.esdl_ids)
        env_vars["connected_services"] = json.dumps(model.connected_services)
        return self.deploy_new_pod(pod_name, model.container_url,[kubernetes.client.V1EnvVar(name, value) for name, value in model.env_vars.items()], labels)

    def delete_model(self, simulator_id: SimulatorId, simulation_id: SimulationId, model_id: ModelId,
                           delete_by: datetime) -> bool:
        if not delete_by or delete_by < datetime.now():
            pod_name = self.model_to_pod_name(simulator_id, simulation_id, model_id)
            LOGGER.info(f'Deleting pod {pod_name}')
            try:
                self.k8s_core_api.delete_namespaced_pod(name=pod_name, namespace=SIMULATION_NAMESPACE)
            except kubernetes.client.ApiException as exc:
                LOGGER.warning(f'Could not remove pod {pod_name}: {exc}')
                success = False
            else:
                success = True
            return success
        return False

    def retrieve_last_log_lines(self,
                                      simulator_id: SimulatorId,
                                      simulation_id: SimulationId,
                                      model_id: ModelId,
                                      num_of_lines: int) -> typing.Optional[str]:
        pod_name = self.model_to_pod_name(simulator_id, simulation_id, model_id)
        LOGGER.info(f'Retrieving last log lines for pod {pod_name}')

        try:
            last_log_lines = self.k8s_core_api.read_namespaced_pod_log(
                                  name=pod_name,
                                  namespace=SIMULATION_NAMESPACE,
                                  follow=False,
                                  tail_lines=num_of_lines)
        except kubernetes.client.ApiException as exc:
            LOGGER.warning(f'Could not retrieve last log lines for pod {pod_name}: {exc}')
            last_log_lines = None
        return last_log_lines

    def list_pods_status_per_simulation_id(self) -> typing.Dict[SimulationId, typing.List[PodStatus]]:
        api_response: kubernetes.client.V1PodList
        api_response = self.k8s_core_api.list_namespaced_pod(namespace=SIMULATION_NAMESPACE)
        result: typing.Dict[SimulationId, typing.List[PodStatus]] = {}

        pod: kubernetes.client.V1Pod
        for pod in api_response.items:
            if 'simulator_id' in pod.metadata.labels:
                simulator_id = pod.metadata.labels['simulator_id']
                sim_id = pod.metadata.labels['simulation_id']
                model_id = pod.metadata.labels['model_id']
                if 'delete_by_datetime' in pod.metadata.labels:
                    delete_by = datetime.fromtimestamp(float(pod.metadata.labels['delete_by_datetime']))
                else:
                    delete_by = None
                if pod.status.container_statuses:
                    container_k8s_status = pod.status.container_statuses[0].state
                else:
                    container_k8s_status = None

                if container_k8s_status:
                    if container_k8s_status.running:
                        model_state = ModelState.RUNNING
                        exit_code = None
                        exit_reason = None
                    elif container_k8s_status.terminated and container_k8s_status.terminated.exit_code == 0:
                        model_state = ModelState.TERMINATED_SUCCESSFULL
                        exit_code = 0
                        exit_reason = 'Success!'
                    elif container_k8s_status.terminated and container_k8s_status.terminated.exit_code != 0:
                        model_state = ModelState.TERMINATED_FAILED
                        exit_code = container_k8s_status.terminated.exit_code
                        exit_reason = container_k8s_status.terminated.reason
                    else:
                        assert container_k8s_status.waiting
                        model_state = ModelState.CREATED
                        exit_code = None
                        exit_reason = None
                else:
                    model_state = ModelState.CREATED
                    exit_code = None
                    exit_reason = None

                result.setdefault(sim_id, []).append(
                    PodStatus(simulator_id, model_id, model_state, exit_code, exit_reason, delete_by))

        return result

    def add_delete_date_to_pods_status_for_simulation_id(self, simulation_id: SimulationId):
        api_response: kubernetes.client.V1PodList
        api_response = self.k8s_core_api.list_namespaced_pod(namespace=SIMULATION_NAMESPACE, label_selector=f"simulation_id={simulation_id}")

        for pod in api_response.items:
            if 'keep_logs_hours' in pod.metadata.labels:
                keep_logs_hours = float(pod.metadata.labels['keep_logs_hours'])
                pod.metadata.labels['delete_by_datetime'] = str(
                    (datetime.now() + timedelta(hours=keep_logs_hours)).timestamp())

                simulator_id = pod.metadata.labels['simulator_id']
                sim_id = pod.metadata.labels['simulation_id']
                model_id = pod.metadata.labels['model_id']

                metadata = {'namespace': SIMULATION_NAMESPACE,
                            'name': self.model_to_pod_name(simulator_id, sim_id, model_id),
                            'labels': pod.metadata.labels}
                body = kubernetes.client.V1Pod(metadata=kubernetes.client.V1ObjectMeta(**metadata))
                self.k8s_core_api.patch_namespaced_pod(self.model_to_pod_name(simulator_id, sim_id, model_id),
                                                       SIMULATION_NAMESPACE,
                                                       body)

    @staticmethod
    def model_to_pod_name(simulator_id: SimulatorId, simulation_id: SimulationId, model_id: ModelId):
        return f'{simulator_id.lower()}-{simulation_id.lower()}-{model_id.lower()}'
