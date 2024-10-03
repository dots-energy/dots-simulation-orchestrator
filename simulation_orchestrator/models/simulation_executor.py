import json
from threading import Thread
import time
from typing import List
from simulation_orchestrator.model_services_orchestrator.k8s_api import K8sApi, HELICS_BROKER_PORT
from simulation_orchestrator.io.log import LOGGER
from dots_infrastructure import Common

import helics as h

from simulation_orchestrator.models.model_inventory import Model
from simulation_orchestrator.models.simulation_inventory import Simulation, SimulationInventory
from simulation_orchestrator.types import ProgressState
from dataclasses import dataclass

@dataclass
class SoFederateInfo:
    federate : h.HelicsFederate
    endpoint : h.HelicsEndpoint
    simulation : Simulation
    terminate_simulation = False

class SimulationExecutor:

    def __init__(self, k8s_api : K8sApi, simulation_inventory : SimulationInventory) -> None:
        self.k8s_api = k8s_api
        self.simulation_inventory = simulation_inventory
        self.simulation_federates : dict[str, SoFederateInfo] = {}

    def _create_new_so_federate_info(self, broker_ip):
        federate_info = h.helicsCreateFederateInfo()
        h.helicsFederateInfoSetBroker(federate_info, broker_ip)
        h.helicsFederateInfoSetTimeProperty(federate_info, h.HelicsProperty.TIME_PERIOD, 60)
        h.helicsFederateInfoSetBrokerPort(federate_info, HELICS_BROKER_PORT)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFederateFlag.UNINTERRUPTIBLE, False)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFederateFlag.WAIT_FOR_CURRENT_TIME_UPDATE, False)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFlag.TERMINATE_ON_ERROR, False)
        h.helicsFederateInfoSetCoreType(federate_info, h.HelicsCoreType.ZMQ)
        h.helicsFederateInfoSetIntegerProperty(federate_info, h.HelicsProperty.INT_LOG_LEVEL, h.HelicsLogLevel.DEBUG)
        return federate_info

    def _send_esdl_file(self, simulation : Simulation, models : List[Model], broker_ip):
        federate_info = self._create_new_so_federate_info(broker_ip)
        LOGGER.info("Creating federate to send esdl file: ")
        message_federate = h.helicsCreateMessageFederate("esdl_broker", federate_info)
        message_enpoint = h.helicsFederateRegisterEndpoint(message_federate, "simulation-orchestrator")
        h.helicsFederateEnterExecutingMode(message_federate)
        esdl_message = h.helicsEndpointCreateMessage(message_enpoint)
        h.helicsMessageSetString(esdl_message, simulation.esdl_base64string)

        request_time = int(h.helicsFederateGetTimeProperty(message_federate, h.HelicsProperty.TIME_PERIOD))
        h.helicsFederateRequestTime(message_federate, request_time)
        for model in models:
            endpoint = f'{model.model_id}/esdl'
            h.helicsMessageSetDestination(esdl_message, endpoint)
            LOGGER.info(f"Sending esdl file to: {endpoint}")
            h.helicsEndpointSendMessage(message_enpoint, esdl_message)

        h.helicsFederateRequestTime(message_federate, h.HELICS_TIME_MAXTIME)
        Common.destroy_federate(message_federate)

    def _init_simulation(self, simulation : Simulation):
        amount_of_helics_federates_esdl_message = sum([calculation_service.nr_of_models for calculation_service in simulation.calculation_services]) + 1 # SO is also a federate that is part of the esdl federation
        amount_of_helics_federates = sum([calculation_service.nr_of_models * calculation_service.amount_of_calculations for calculation_service in simulation.calculation_services]) + 1 # SO is also a federate that is part of the federation
        models = simulation.model_inventory.get_models()
        broker_ip = self.k8s_api.deploy_helics_broker(amount_of_helics_federates, amount_of_helics_federates_esdl_message, simulation.simulation_id, simulation.simulator_id)
        calculation_service_names = [calculation_service.esdl_type for calculation_service in simulation.calculation_services]
        for model in models:
            self.k8s_api.deploy_model(simulation, model, broker_ip, calculation_service_names)
            self.k8s_api.await_pod_to_running_state(self.k8s_api.model_to_pod_name(simulation.simulator_id, simulation.simulation_id, model.model_id))

        self._send_esdl_file(simulation, models, broker_ip)
        self.simulation_inventory.set_state_for_all_models(simulation.simulation_id, ProgressState.DEPLOYED)
        return broker_ip

    def _create_so_federate(self, broker_ip : str, simulation : Simulation):
        federate_info = self._create_new_so_federate_info(broker_ip)
        message_federate = h.helicsCreateMessageFederate(f"so-{simulation.simulation_id}", federate_info)
        message_enpoint = h.helicsFederateRegisterEndpoint(message_federate, "commands")
        return SoFederateInfo(message_federate, message_enpoint, simulation)
    
    def _terminate_simulation_loop(self, so_federate_info : SoFederateInfo):
        message_endpoint = so_federate_info.endpoint
        federate = so_federate_info.federate
        h.helicsFederateEnterExecutingMode(federate)
        total_interval = so_federate_info.simulation.simulation_duration_in_seconds
        update_interval = int(h.helicsFederateGetTimeProperty(federate, h.HELICS_PROPERTY_TIME_PERIOD))
        grantedtime = 0
        terminate_requested = False
        while not so_federate_info.terminate_simulation and grantedtime < total_interval and not terminate_requested:
            requested_time = grantedtime + update_interval
            grantedtime = h.helicsFederateRequestTime(federate, requested_time)
            terminate_requested = Common.terminate_requested_at_commands_endpoint(message_endpoint)

        if so_federate_info.terminate_simulation:
            Common.terminate_simulation(federate, message_endpoint)

        Common.destroy_federate(federate)
        self.simulation_inventory.set_state_for_all_models(so_federate_info.simulation.simulation_id, ProgressState.TERMINATED_SUCCESSFULL)
        if self.simulation_inventory.is_active_simulation_from_queue(so_federate_info.simulation.simulation_id):
            self.simulation_inventory.pop_simulation_in_queue()
            if self.simulation_inventory.nr_of_queued_simulations() > 0:
                next_simulation_id = self.simulation_inventory.get_active_simulation_in_queue()
                next_simulation = self.simulation_inventory.get_simulation(next_simulation_id)
                self._deploy_simulation(next_simulation)

    def _deploy_simulation(self, simulation : Simulation):
        broker_ip = self._init_simulation(simulation)
        time.sleep(2)
        self.simulation_federates[simulation.simulation_id] = self._create_so_federate(broker_ip, simulation)
        self._terminate_simulation_loop(self.simulation_federates[simulation.simulation_id])

    def deploy_simulation(self, simulation : Simulation):
        thread = Thread(target = self._deploy_simulation, args = [simulation])
        thread.start()

    def terminate_simulation(self, simulation_id : str):
        self.simulation_federates[simulation_id].terminate_simulation = True
