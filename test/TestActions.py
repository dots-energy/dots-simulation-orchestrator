from datetime import datetime
import unittest
from unittest.mock import MagicMock

from simulation_orchestrator import actions, parse_esdl
from simulation_orchestrator.dataclasses.CalculationServiceInfo import CalculationServiceInfo
from simulation_orchestrator.simulation_logic.model_inventory import Model
from simulation_orchestrator.simulation_logic.simulation_executor import SimulationExecutor
from simulation_orchestrator.simulation_logic.simulation_inventory import SimulationInventory
from simulation_orchestrator.rest.schemas.SimulationPost import SimulationPost
from simulation_orchestrator.types import ProgressState


class TestActions(unittest.TestCase):

    def setUp(self):
        self.simulation_post = SimulationPost(calculation_services=[])
        self.simulation_post.name = "test-name"
        self.simulation_post.start_date = datetime(2024,1,1)
        self.simulation_post.simulation_duration_in_seconds = 86400
        self.simulation_post.keep_logs_hours = 24.0
        self.simulation_post.log_level = 'info'
        self.simulation_post.calculation_services = []
        self.simulation_post.calculation_services = ''
        actions.simulation_inventory = SimulationInventory()
        actions.simulation_executor = SimulationExecutor(None, actions.simulation_inventory)
        self.parse_esdl_get_model_list = parse_esdl.get_model_list
        self.parse_esdl_get_energy_system = parse_esdl.get_energy_system
        self.actions_simulation_executor = actions.simulation_executor.deploy_simulation
        actions.simulation_executor.deploy_simulation = MagicMock()
        self.mock_model = Model("test", ["test"], CalculationServiceInfo("test", "test", 1, 1, "test", ["test"], []), ProgressState.DEPLOYED)
        parse_esdl.get_model_list = MagicMock(return_value=[self.mock_model])
        parse_esdl.get_energy_system = MagicMock(return_value=None)

    def tearDown(self) -> None:
        parse_esdl.get_model_list = self.parse_esdl_get_model_list
        parse_esdl.get_energy_system = self.parse_esdl_get_energy_system
        actions.simulation_executor.deploy_simulation = self.actions_simulation_executor

    def test_start_simulations_registers_and_deploys_simulation_correctly(self):
        # execute
        simulation_id = actions.start_new_simulation(self.simulation_post)
        models = actions.simulation_inventory.get_models_from_simulation(simulation_id)

        # assert
        self.assertEqual(len(actions.simulation_inventory.activeSimulations), 1)
        self.assertListEqual(models, [self.mock_model])
        actions.simulation_executor.deploy_simulation.assert_called_once()

    def test_queue_simulation_adds_simulation_to_queue(self):
        # execute
        simulation_id = actions.queue_new_simulation(self.simulation_post)
        simulation_id_2 = actions.queue_new_simulation(self.simulation_post)

        # assert
        nr_queued_simulations = actions.simulation_inventory.nr_of_queued_simulations()

        self.assertEqual(nr_queued_simulations, 2)
        self.assertEqual(actions.simulation_inventory.simulationQueue, [simulation_id, simulation_id_2])

    def test_queue_simulation_deploys_simulation_when_queue_is_empty(self):
        # execute
        actions.queue_new_simulation(self.simulation_post)

        # assert
        actions.simulation_executor.deploy_simulation.assert_called_once()


if __name__ == '__main__':
    unittest.main()