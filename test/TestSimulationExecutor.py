from datetime import datetime
import unittest
from unittest.mock import MagicMock
import helics as h
from simulation_orchestrator.models.simulation_executor import SimulationExecutor, SoFederateInfo
from simulation_orchestrator.models.simulation_inventory import Simulation, SimulationInventory
from simulation_orchestrator.models.model_inventory import Model
from simulation_orchestrator.types import ProgressState
from dots_infrastructure import Common

class TestSimulationExecutor(unittest.TestCase):

    def setUp(self):
        self.helicsFederateEnterExecutingMode = h.helicsFederateEnterExecutingMode
        self.helicsFederateGetTimeProperty = h.helicsFederateGetTimeProperty
        self.common_terminate_simulation = Common.terminate_simulation
        self.common_destroy_federate = Common.destroy_federate
        h.helicsFederateEnterExecutingMode = MagicMock()
        h.helicsFederateGetTimeProperty = MagicMock(return_value=3)
        Common.terminate_simulation = MagicMock()
        Common.destroy_federate = MagicMock()
        self.simulation_inventory = SimulationInventory()
        self.simulation = Simulation("test","test-name", datetime(2024,1,1), 900, 2.0, "DEBUG",[], "")

    def tearDown(self) -> None:
        h.helicsFederateEnterExecutingMode = self.helicsFederateEnterExecutingMode
        h.helicsFederateGetTimeProperty = self.helicsFederateGetTimeProperty
        Common.terminate_simulation = self.common_terminate_simulation
        Common.destroy_federate = self.common_destroy_federate

    def test_simulation_is_termintad_when_time_has_passed(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.add_simulation(self.simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(None, self.simulation_inventory)
        so_federate_info = SoFederateInfo(None, None, self.simulation_inventory.get_simulation(active_simulation_id))
        Common.terminate_requested_at_commands_endpoint = MagicMock(return_value=False)
        h.helicsFederateRequestTime = MagicMock(return_value=h.HELICS_TIME_MAXTIME)

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        # Assert
        Common.destroy_federate.assert_called_once()
        Common.terminate_simulation.assert_not_called()
        self.assertEqual(self.simulation_inventory.get_simulation_state(active_simulation_id), ProgressState.TERMINATED_SUCCESSFULL)

    def test_simulation_is_termintad_when_terminate_is_requested_from_endpoint(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.add_simulation(self.simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(None, self.simulation_inventory)
        so_federate_info = SoFederateInfo(None, None, self.simulation_inventory.get_simulation(active_simulation_id))
        Common.terminate_requested_at_commands_endpoint = MagicMock(return_value=True)
        h.helicsFederateRequestTime = MagicMock(return_value=500)

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        # Assert
        Common.destroy_federate.assert_called_once()
        Common.terminate_simulation.assert_not_called()
        self.assertEqual(self.simulation_inventory.get_simulation_state(active_simulation_id), ProgressState.TERMINATED_SUCCESSFULL)

    def test_simulation_is_termintad_when_terminate_is_requested_from_api(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.add_simulation(self.simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(None, self.simulation_inventory)
        so_federate_info = SoFederateInfo(None, None, self.simulation_inventory.get_simulation(active_simulation_id))
        so_federate_info.terminate_simulation = True
        Common.terminate_requested_at_commands_endpoint = MagicMock(return_value=False)
        h.helicsFederateRequestTime = MagicMock(return_value=500)

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        # Assert
        Common.destroy_federate.assert_called_once()
        Common.terminate_simulation.assert_called_once()
        self.assertEqual(self.simulation_inventory.get_simulation_state(active_simulation_id), ProgressState.TERMINATED_SUCCESSFULL)

    def test_next_simulation_in_queue_is_started_when_active_simulation_is_terminated(self):
        # Arrange
        active_simulation_id = self.simulation_inventory.queue_simulation(self.simulation)
        next_queued_simulation = Simulation("test2","test-name2", datetime(2024,1,1), 900, 2.0, "DEBUG",[], "")
        next_queued_simulation_id = self.simulation_inventory.queue_simulation(next_queued_simulation)
        self.simulation.model_inventory.add_models_to_simulation(self.simulation.simulation_id, [Model("test", ["test"], "test", "test", "test", ProgressState.DEPLOYED, [])])
        simulation_executor = SimulationExecutor(None, self.simulation_inventory)
        so_federate_info = SoFederateInfo(None, None, self.simulation_inventory.get_simulation(active_simulation_id))
        Common.terminate_requested_at_commands_endpoint = MagicMock(return_value=False)
        h.helicsFederateRequestTime = MagicMock(return_value=h.HELICS_TIME_MAXTIME)
        simulation_executor._deploy_simulation = MagicMock()

        # Execute
        simulation_executor._terminate_simulation_loop(so_federate_info)

        self.assertEqual(self.simulation_inventory.nr_of_queued_simulations(), 1)
        self.assertEqual(self.simulation_inventory.get_active_simulation_in_queue(), next_queued_simulation_id)
        simulation_executor._deploy_simulation.assert_called_once_with(next_queued_simulation)

if __name__ == '__main__':
    unittest.main()