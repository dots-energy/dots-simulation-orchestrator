from io import BytesIO
from threading import Thread
import time
from typing import List
import zipfile
from simulation_orchestrator.model_services_orchestrator.k8s_api import (
    K8sApi,
    HELICS_BROKER_PORT,
)
from simulation_orchestrator.io.log import LOGGER
import helics as h

from simulation_orchestrator.model_services_orchestrator.types import ModelState
from simulation_orchestrator.simulation_logic.model_inventory import Model
from simulation_orchestrator.simulation_logic.simulation_inventory import (
    Simulation,
    SimulationInventory,
)
from simulation_orchestrator.types import ProgressState
from dataclasses import dataclass


@dataclass
class SoFederateInfo:
    simulation: Simulation
    terminate_requeted_by_user = False


class SimulationExecutor:
    def __init__(
        self, k8s_api: K8sApi, simulation_inventory: SimulationInventory
    ) -> None:
        self.k8s_api = k8s_api
        self.simulation_inventory = simulation_inventory
        self.simulation_book: dict[str, SoFederateInfo] = {}

    def _create_new_so_federate_info(self, broker_ip):
        federate_info = h.helicsCreateFederateInfo()
        h.helicsFederateInfoSetBroker(federate_info, broker_ip)
        h.helicsFederateInfoSetBrokerPort(federate_info, HELICS_BROKER_PORT)
        h.helicsFederateInfoSetCoreType(federate_info, h.HelicsCoreType.ZMQ)
        h.helicsFederateInfoSetIntegerProperty(
            federate_info, h.HelicsProperty.INT_LOG_LEVEL, h.HelicsLogLevel.DEBUG
        )
        return federate_info

    def _send_esdl_file(self, simulation: Simulation, models: List[Model], broker_ip):
        federate_info = self._create_new_so_federate_info(broker_ip)
        LOGGER.info("Creating federate to send esdl file: ")
        message_federate = h.helicsCreateMessageFederate(
            f"{simulation.simulation_id}-esdl_broker", federate_info
        )
        message_enpoint = h.helicsFederateRegisterEndpoint(
            message_federate, "simulation-orchestrator"
        )
        step_size = 10000000

        h.helicsFederateEnterExecutingMode(message_federate)
        for i in range(0, len(simulation.esdl_base64string), step_size):
            FEDERATE_OFFSET = 2
            time_to_request = i / step_size + FEDERATE_OFFSET
            h.helicsFederateRequestTime(message_federate, time_to_request)
            esdl_message = h.helicsEndpointCreateMessage(message_enpoint)
            esdl_file_part = simulation.esdl_base64string[i : i + step_size]
            LOGGER.info(
                f"Sending part {i / step_size} of esdl file with: {len(esdl_file_part)} characters"
            )
            h.helicsMessageSetData(esdl_message, esdl_file_part.encode())
            for model in models:
                endpoint = f"{model.model_id}/esdl"
                h.helicsMessageSetDestination(esdl_message, endpoint)
                LOGGER.info(f"Sending esdl file to: {endpoint}")
                h.helicsEndpointSendMessage(message_enpoint, esdl_message)

        h.helicsFederateRequestTime(message_federate, h.HELICS_TIME_MAXTIME)
        h.helicsFederateDisconnect(message_federate)
        h.helicsFederateDestroy(message_federate)

    def _init_simulation(self, simulation: Simulation):
        models = simulation.model_inventory.get_models()
        amount_of_helics_federates_initialization_stage = len(models) + 1
        broker_ip = self.k8s_api.deploy_helics_broker(
            amount_of_helics_federates_initialization_stage,
            simulation.simulation_id,
            simulation.simulator_id,
        )
        calculation_service_names = [
            calculation_service.esdl_type
            for calculation_service in simulation.calculation_services
        ]
        for model in models:
            self.k8s_api.deploy_model(
                simulation, model, broker_ip, calculation_service_names
            )
            self.k8s_api.await_pod_to_running_state(
                self.k8s_api.model_to_pod_name(
                    simulation.simulator_id, simulation.simulation_id, model.model_id
                )
            )

        self._send_esdl_file(simulation, models, broker_ip)
        self.simulation_inventory.set_state_for_all_models(
            simulation.simulation_id, ProgressState.DEPLOYED
        )
        return SoFederateInfo(simulation)

    def _terminate_simulation_loop(self, so_federate_info: SoFederateInfo):
        terminate_requested_by_user = False
        terminated_because_of_error = False
        terminated_because_of_succesfull_finish = False
        while (
            not terminate_requested_by_user
            and not terminated_because_of_error
            and not terminated_because_of_succesfull_finish
        ):
            terminate_requested_by_user = so_federate_info.terminate_requeted_by_user
            pod_statuses = self.k8s_api.list_pods_status_per_simulation_id()
            pod_status_simulation = pod_statuses[
                so_federate_info.simulation.simulation_id
            ]
            terminated_because_of_error = any(
                pod_status.model_state == ModelState.TERMINATED_FAILED
                for pod_status in pod_status_simulation
            )
            terminated_because_of_succesfull_finish = all(
                pod_status.model_state == ModelState.TERMINATED_SUCCESSFULL
                for pod_status in pod_status_simulation
            )

            time.sleep(1)

        if terminated_because_of_error:
            self.simulation_inventory.set_state_for_all_models(
                so_federate_info.simulation.simulation_id,
                ProgressState.TERMINATED_FAILED,
            )
        elif terminated_because_of_succesfull_finish:
            self.simulation_inventory.set_state_for_all_models(
                so_federate_info.simulation.simulation_id,
                ProgressState.TERMINATED_SUCCESSFULL,
            )
        elif terminate_requested_by_user:
            self.delete_all_pods_from_simulation(so_federate_info.simulation)

        self._start_next_simulation_in_queue(so_federate_info)

    def delete_all_pods_from_simulation(self, simulation: Simulation):
        for model in simulation.model_inventory.get_models():
            self.k8s_api.delete_pod_with_model(model)
        self.k8s_api.delete_broker_pod_of_simulation_id(simulation.simulation_id)
        simulation_state = self.simulation_inventory.get_simulation_state(
            simulation.simulation_id
        )
        if simulation_state == ProgressState.TERMINATED_SUCCESSFULL:
            self.simulation_inventory.set_state_for_all_models(
                simulation.simulation_id,
                ProgressState.TERMINATED_SUCCESSFULL_POD_DELETED,
            )
        elif simulation_state == ProgressState.TERMINATED_FAILED:
            self.simulation_inventory.set_state_for_all_models(
                simulation.simulation_id,
                ProgressState.TERMINATED_FAILED_POD_DELETED,
            )
        else:
            self.simulation_inventory.set_state_for_all_models(
                simulation.simulation_id,
                ProgressState.POD_DELETED,
            )

    def get_all_logs_from_simulation(self, simulation: Simulation) -> BytesIO | None:
        log_output = {}
        for model in simulation.model_inventory.get_models():
            if (
                model.current_state != ProgressState.POD_DELETED
                and model.current_state
                != ProgressState.TERMINATED_SUCCESSFULL_POD_DELETED
            ):
                pod_name = self.k8s_api.model_to_pod_name(
                    simulation.simulator_id, simulation.simulation_id, model.model_id
                )
                log_output[pod_name] = self.k8s_api.get_logs_of_pod_with_model(model)

        has_data = len(log_output) > 0
        zip_buffer = BytesIO()

        if has_data:
            with zipfile.ZipFile(
                file=zip_buffer,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            ) as zip_archive:
                for file_name, logs in log_output.items():
                    if logs != "":
                        zip_archive.writestr(
                            zinfo_or_arcname=f"{file_name}.log",
                            data=logs,
                        )

            zip_buffer.seek(0)

        return zip_buffer if has_data else None

    def _create_so_federate(self, broker_ip: str, simulation: Simulation):
        federate_info = self._create_new_so_federate_info(broker_ip)
        message_federate = h.helicsCreateMessageFederate(
            f"so-{simulation.simulation_id}", federate_info
        )
        message_enpoint = h.helicsFederateRegisterEndpoint(message_federate, "commands")
        return SoFederateInfo(message_federate, message_enpoint, simulation)

    def _start_next_simulation_in_queue(self, so_federate_info: SoFederateInfo):
        if self.simulation_inventory.is_active_simulation_from_queue(
            so_federate_info.simulation.simulation_id
        ):
            self.simulation_inventory.pop_simulation_in_queue()
            if self.simulation_inventory.nr_of_queued_simulations() > 0:
                next_simulation_id = (
                    self.simulation_inventory.get_active_simulation_in_queue()
                )
                next_simulation = self.simulation_inventory.get_simulation(
                    next_simulation_id
                )
                self._deploy_simulation(next_simulation)

    def _deploy_simulation(self, simulation: Simulation):
        self.simulation_book[simulation.simulation_id] = self._init_simulation(
            simulation
        )
        self._terminate_simulation_loop(self.simulation_book[simulation.simulation_id])

    def deploy_simulation(self, simulation: Simulation):
        thread = Thread(target=self._deploy_simulation, args=[simulation])
        thread.start()

    def terminate_simulation(self, simulation_id: str):
        self.simulation_book[simulation_id].terminate_requeted_by_user = True
