#!/usr/bin/env python
import json
import threading
import typing
import sched
import time
from datetime import datetime

from paho.mqtt.client import Client

import messages as messages
from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.models.simulation_inventory import SimulationInventory
from simulation_orchestrator.types import SimulationId, SimulatorId, ProgressState

MODEL_PARAMETERS = 'model_parameters'
NEW_STEP = 'new_step'
STOP_SERVICE = 'stop_service'


class MqttClient:
    def __init__(self, host: str, port: int, qos: int, username: str, password: str, influxdb_host: str,
                 influxdb_port: str, influxdb_user: str, influxdb_password: str, influxdb_name: str,
                 simulation_inventory: SimulationInventory):
        self.host = host
        self.port = port
        self.qos = qos
        self.username = username
        self.password = password
        self.influxdb_host = influxdb_host
        self.influxdb_port = influxdb_port
        self.influxdb_user = influxdb_user
        self.influxdb_password = influxdb_password
        self.influxdb_name = influxdb_name

        self.simulation_inventory = simulation_inventory

        self.mqtt_client = None
        self.subscribed_topics = []

    def start(self):
        # initialize mqtt connection
        self.mqtt_client = Client(clean_session=True)

        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            # print("Connected with result code " + str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            for topic in self.subscribed_topics:
                client.subscribe(topic, self.qos)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            threading.Thread(target=self._process_message, args=[client, msg]).start()

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message

        self.mqtt_client.username_pw_set(self.username, self.password)
        self.connect()

        self._subscribe_lifecycle_topics()

        # Check if the step calculations don't exceed the limit
        threading.Thread(target=self._check_step_calc_time, args=[]).start()

        LOGGER.debug('Simulation Orchestrator connected to MQTT broker.')
        self.mqtt_client.loop_forever()

    def connect(self):
        try:
            self.mqtt_client.connect(self.host, port=self.port)
        except Exception as e:
            LOGGER.debug("Could not connect to MQTT broker, retry in 2 seconds: {}".format(e))
            time.sleep(2)
            self.connect()

    def _check_step_calc_time(self):
        s = sched.scheduler(time.time, time.sleep)

        def check_calc_time(sc):
            for simulation_id in self.simulation_inventory.get_simulation_ids_exceeding_step_calc_time():
                self.send_simulation_done(simulation_id)
            sc.enter(10, 1, check_calc_time, (sc,))

        s.enter(10, 1, check_calc_time, (s,))
        s.run()

    def _process_message(self, client: Client, message):
        topic_parts = message.topic.split('/')
        LOGGER.info(f" [received] {message.topic}: {message.payload}")

        if topic_parts[5] == 'ModelsReady':
            simulation_id = topic_parts[4]
            self.simulation_inventory.lock_simulation(simulation_id)

            for model in self.simulation_inventory.get_all_models(simulation_id):
                model.current_state = ProgressState.DEPLOYED
            self._send_model_parameters(simulation_id)

            self.simulation_inventory.release_simulation(simulation_id)
        if len(topic_parts) > 6:
            simulation_id = topic_parts[4]
            self.simulation_inventory.lock_simulation(simulation_id)

            model_id = topic_parts[5]
            if topic_parts[6] == 'ErrorOccurred':
                self.simulation_inventory.set_state_for_all_models(
                    simulation_id=simulation_id,
                    new_state=ProgressState.TERMINATED_SUCCESSFULL
                )
                error_occurred = messages.ErrorOccurred()
                error_occurred.ParseFromString(message.payload)
                self.simulation_inventory.error_message = error_occurred.error_message
            elif topic_parts[6] == 'Parameterized' or topic_parts[6] == 'CalculationsDone':
                if topic_parts[6] == 'Parameterized':
                    new_model_state = ProgressState.PARAMETERIZED
                else:
                    new_model_state = ProgressState.STEP_FINISHED

                simulation_state = self.simulation_inventory.update_model_state_and_get_simulation_state(
                    simulation_id=simulation_id,
                    model_id=model_id,
                    new_state=new_model_state
                )
                if simulation_state == new_model_state:
                    if self.simulation_inventory.on_last_time_step(simulation_id):
                        self.simulation_inventory.set_state_for_all_models(
                            simulation_id=simulation_id,
                            new_state=ProgressState.TERMINATED_SUCCESSFULL
                        )
                        self.send_simulation_done(simulation_id)
                        LOGGER.info(f"All time steps finished for simulation '{simulation_id}'")
                        if self.simulation_inventory.is_active_simulation_from_queue(simulation_id):
                            self.simulation_inventory.pop_simulation_in_queue()
                            if self.simulation_inventory.nr_of_queued_simulations() > 0:
                                next_simulation_in_queue = self.simulation_inventory.get_simulation(simulation_id)
                                LOGGER.info(f"Starting next simulation in queue with simulation_id: '{next_simulation_in_queue.simulation_id}'")
                                self.send_deploy_models(next_simulation_in_queue.simulator_id, next_simulation_in_queue.simulation_id,
                                            next_simulation_in_queue.keep_logs_hours, next_simulation_in_queue.log_level)
                    else:
                        self._send_new_step(simulation_id)

            self.simulation_inventory.release_simulation(simulation_id)

    def _subscribe_lifecycle_topics(self):
        topics = [
            f'/lifecycle/mso/dots-so/#',
            f'/lifecycle/model/dots-so/#'
        ]
        for topic in topics:
            self.mqtt_client.subscribe(topic, self.qos)
            self.subscribed_topics.append(topic)

    def send_deploy_models(self, simulator_id: SimulatorId, simulation_id: SimulationId, keep_logs_hours: float,
                           log_level: typing.Union[int, str]):
        model_configs = []
        for model in self.simulation_inventory.get_all_models(simulation_id):
            pod_name = f'{simulator_id.lower()}-{simulation_id.lower()}-{model.model_id}'
            if len(pod_name) > 62:
                raise IOError(f"Pod name is too long for Kubernetes '{pod_name}' (max 63 characters)")
            env_vars = [
                messages.EnvironmentVariable(name='MQTT_HOST', value=str(self.host)),
                messages.EnvironmentVariable(name='MQTT_PORT', value=str(self.port)),
                messages.EnvironmentVariable(name='MQTT_QOS', value=str(self.qos)),
                messages.EnvironmentVariable(name='SIMULATOR_ID', value=simulator_id),
                messages.EnvironmentVariable(name='SIMULATION_ID', value=simulation_id),
                messages.EnvironmentVariable(name='MODEL_ID', value=model.model_id),
                messages.EnvironmentVariable(name='MQTT_USERNAME', value=self.username),
                messages.EnvironmentVariable(name='MQTT_PASSWORD', value=self.password),
                messages.EnvironmentVariable(name='INFLUXDB_HOST', value=self.influxdb_host),
                messages.EnvironmentVariable(name='INFLUXDB_PORT', value=self.influxdb_port),
                messages.EnvironmentVariable(name='INFLUXDB_USER', value=self.influxdb_user),
                messages.EnvironmentVariable(name='INFLUXDB_PASSWORD', value=self.influxdb_password),
                messages.EnvironmentVariable(name='INFLUXDB_NAME', value=self.influxdb_name),
                messages.EnvironmentVariable(name='LOG_LEVEL', value=log_level.upper())
            ]
            model_configs.append(messages.ModelConfiguration(
                modelID=model.model_id,
                imageUrl=model.service_image_url,
                environmentVariables=env_vars)
            )
            self.mqtt_client.subscribe(f"/log/model/dots-so/{simulation_id}/{model.model_id}")
        message = messages.DeployModels(
            simulatorId=simulator_id,
            modelConfigurations=model_configs,
            keepLogsHours=keep_logs_hours,
        )
        topic = f'/lifecycle/dots-so/mso/{simulation_id}/DeployModels'
        self.mqtt_client.publish(topic, message.SerializeToString())
        LOGGER.info(f" [sent] {topic}")

    def _send_model_parameters(self, simulation_id: SimulationId):
        simulation = self.simulation_inventory.get_simulation(simulation_id)
        for model in self.simulation_inventory.get_all_models(simulation_id):
            model_parameters_message = messages.ModelParameters(
                parameters_dict=json.dumps({
                    'simulation_name': simulation.simulation_name,
                    'start_timestamp': simulation.simulation_start_datetime.timestamp(),
                    'time_step_seconds': simulation.time_step_seconds,
                    'nr_of_time_steps': simulation.nr_of_time_steps,
                    'calculation_services': simulation.calculation_services,
                    'esdl_base64string': simulation.esdl_base64string,
                    'esdl_ids': model.esdl_ids,
                })
            )
            self.mqtt_client.publish(
                topic=f"/lifecycle/dots-so/model/{simulation_id}/{model.model_id}/ModelParameters",
                payload=model_parameters_message.SerializeToString()
            )
        LOGGER.info(f" [sent] lifecycle/dots-so/model/{simulation_id}/+/ModelParameters")

    def _send_new_step(self, simulation_id: SimulationId):
        self.simulation_inventory.set_state_for_all_models(simulation_id, ProgressState.STEP_STARTED)

        start_end_date_dict = self.simulation_inventory.increment_time_step_and_get_time_start_end_date_dict(
            simulation_id)

        new_step_message = messages.NewStep(
            parameters_dict=json.dumps(start_end_date_dict)
        )
        for model in self.simulation_inventory.get_all_models(simulation_id):
            self.mqtt_client.publish(
                topic=f"/lifecycle/dots-so/model/{simulation_id}/{model.model_id}/NewStep",
                payload=new_step_message.SerializeToString()
            )
        LOGGER.debug(f" [sent] lifecycle/dots-so/model/{simulation_id}/+/NewStep")
        self.simulation_inventory.start_step_calculation_time_counting(simulation_id)

    def send_simulation_done(self, simulation_id: SimulationId):
        for model in self.simulation_inventory.get_all_models(simulation_id):
            self.mqtt_client.publish(
                topic=f"/lifecycle/dots-so/model/{simulation_id}/{model.model_id}/SimulationDone",
                payload=messages.SimulationDone().SerializeToString()
            )
        LOGGER.info(f" [sent] lifecycle/dots-so/model/{simulation_id}/+/SimulationDone")
        self.simulation_inventory.get_simulation(simulation_id).terminated = True
        self.simulation_inventory.get_simulation(simulation_id).calculation_end_datetime = datetime.now()
