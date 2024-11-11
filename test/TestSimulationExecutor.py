from datetime import datetime
import unittest
from unittest.mock import MagicMock
import helics as h
from simulation_orchestrator.model_services_orchestrator.k8s_api import K8sApi, PodStatus
from simulation_orchestrator.model_services_orchestrator.types import ModelState
from simulation_orchestrator.simulation_logic.simulation_executor import SimulationExecutor, SoFederateInfo
from simulation_orchestrator.simulation_logic.simulation_inventory import Simulation, SimulationInventory
from simulation_orchestrator.simulation_logic.model_inventory import Model
from simulation_orchestrator.types import ProgressState

class TestSimulationExecutor(unittest.TestCase):

    def setUp(self):
        self.helicsFederateEnterExecutingMode = h.helicsFederateEnterExecutingMode
        self.helicsFederateGetTimeProperty = h.helicsFederateGetTimeProperty
        self.helicsFederateRequestTime = h.helicsFederateRequestTime
        h.helicsFederateEnterExecutingMode = MagicMock()
        h.helicsFederateGetTimeProperty = MagicMock(return_value=3)
        self.simulation_inventory = SimulationInventory()
        self.simulation = Simulation("test","test-name", datetime(2024,1,1), 900, 2.0, "DEBUG",[], "")

    def tearDown(self) -> None:
        h.helicsFederateEnterExecutingMode = self.helicsFederateEnterExecutingMode
        h.helicsFederateGetTimeProperty = self.helicsFederateGetTimeProperty
        h.helicsFederateRequestTime = self.helicsFederateRequestTime

    def test_simulation_state_is_set_to_succesfull_when_all_pods_have_success_state(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.add_simulation(self.simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(K8sApi(None, {}), self.simulation_inventory)
        pod_status_dict = {
            active_simulation_id : [
                PodStatus("SO", "test", ModelState.TERMINATED_SUCCESSFULL, 0, None, None )
            ]
        }
        simulation_executor.k8s_api.list_pods_status_per_simulation_id = MagicMock(return_value=pod_status_dict)
        so_federate_info = SoFederateInfo(self.simulation_inventory.get_simulation(active_simulation_id))

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        # Assert
        self.assertEqual(self.simulation_inventory.get_simulation_state(active_simulation_id), ProgressState.TERMINATED_SUCCESSFULL)

    def test_simulation_is_termintad_when_pod_has_a_failed_status(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.add_simulation(self.simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(K8sApi(None, {}), self.simulation_inventory)
        pod_status_dict = {
            active_simulation_id : [
                PodStatus("SO", "test", ModelState.TERMINATED_FAILED, 1, "Exception", None )
            ]
        }
        simulation_executor.k8s_api.list_pods_status_per_simulation_id = MagicMock(return_value=pod_status_dict)
        simulation_executor.k8s_api.delete_broker_pod_of_simulation_id = MagicMock()
        simulation_executor.k8s_api.delete_pod_with_model_id = MagicMock()
        so_federate_info = SoFederateInfo(self.simulation_inventory.get_simulation(active_simulation_id))

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        # Assert
        self.assertEqual(self.simulation_inventory.get_simulation_state(active_simulation_id), ProgressState.TERMINATED_FAILED)

    def test_simulation_is_termintad_and_pods_are_deleted_when_terminate_is_requested_from_api(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.add_simulation(self.simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(K8sApi(None, {}), self.simulation_inventory)
        so_federate_info = SoFederateInfo(self.simulation_inventory.get_simulation(active_simulation_id))
        so_federate_info.terminate_requeted_by_user = True
        pod_status_dict = {
            active_simulation_id : [
                PodStatus("SO", "test", ModelState.RUNNING, None, None, None )
            ]
        }
        simulation_executor.k8s_api.list_pods_status_per_simulation_id = MagicMock(return_value=pod_status_dict)
        simulation_executor.k8s_api.delete_broker_pod_of_simulation_id = MagicMock()
        simulation_executor.k8s_api.delete_pod_with_model_id = MagicMock()

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        # Assert
        simulation_executor.k8s_api.delete_broker_pod_of_simulation_id.assert_called_once_with(active_simulation_id)
        simulation_executor.k8s_api.delete_pod_with_model_id.assert_called_once_with("test", active_simulation_id, "test")
        self.assertEqual(self.simulation_inventory.get_simulation_state(active_simulation_id), ProgressState.TERMINATED_SUCCESSFULL)

    def test_next_simulation_in_queue_is_started_when_active_simulation_is_terminated(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.queue_simulation(self.simulation)
        next_queued_simulation = Simulation("test2","test-name2", datetime(2024,1,1), 900, 2.0, "DEBUG",[], "")
        next_queued_simulation_id = self.simulation_inventory.queue_simulation(next_queued_simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(K8sApi(None, {}), self.simulation_inventory)
        pod_status_dict = {
            active_simulation_id : [
                PodStatus("SO", "test", ModelState.TERMINATED_SUCCESSFULL, 0, None, None )
            ]
        }
        simulation_executor.k8s_api.list_pods_status_per_simulation_id = MagicMock(return_value=pod_status_dict)
        so_federate_info = SoFederateInfo(self.simulation_inventory.get_simulation(active_simulation_id))
        simulation_executor._deploy_simulation = MagicMock()

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        self.assertEqual(self.simulation_inventory.nr_of_queued_simulations(), 1)
        self.assertEqual(self.simulation_inventory.get_active_simulation_in_queue(), next_queued_simulation_id)
        simulation_executor._deploy_simulation.assert_called_once_with(next_queued_simulation)

if __name__ == '__main__':
    unittest.main()