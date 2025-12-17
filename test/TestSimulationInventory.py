from datetime import datetime
import unittest
from simulation_orchestrator.dataclasses.CalculationServiceInfo import (
    CalculationServiceInfo,
)
from simulation_orchestrator.simulation_logic.model_inventory import Model
from simulation_orchestrator.simulation_logic.simulation_inventory import (
    Simulation,
    SimulationInventory,
)
from simulation_orchestrator.types import ProgressState


class TestSimulationExecutor(unittest.TestCase):
    simulations_to_test = {
        Simulation(
            "test", "hello world!", datetime(2024, 1, 1), 900, 2.0, "DEBUG", [], ""
        ): "hello-world",
        Simulation(
            "test",
            "--test^&*&#)( name---",
            datetime(2024, 1, 1),
            900,
            2.0,
            "DEBUG",
            [],
            "",
        ): "test-name",
    }

    def test_simulation_ids_do_not_contain_illegal_characters(self):
        for (
            simulation,
            expected_simulation_id_substring,
        ) in self.simulations_to_test.items():
            with self.subTest(state=expected_simulation_id_substring):
                # Arrange
                simulation_inventory = SimulationInventory()

                # Act
                simulation_id = simulation_inventory.add_simulation(simulation)

                # Assert
                self.assertIn(
                    expected_simulation_id_substring,
                    simulation_id,
                )

    models_to_test = [
        Model(
            "model1",
            1,
            ["esdl1"],
            CalculationServiceInfo("test-name", "test-url", 4, 2, "pv", ["bla"], []),
            ProgressState.REGISTERED,
        ),
        Model(
            "model2",
            1,
            ["esdl1"],
            CalculationServiceInfo(
                "test-name_dase-way-to-long-name-jala-ajdas-jeasfd",
                "test-url",
                4,
                2,
                "pv",
                ["bla"],
                [],
            ),
            ProgressState.REGISTERED,
        ),
    ]

    def test_pod_names_meet_the_RFC_1123_standard(self):
        for model in self.models_to_test:
            with self.subTest(state=model.model_id):
                # Arrange
                simulation_inventory = SimulationInventory()
                simulation = Simulation(
                    "test",
                    "hello world!",
                    datetime(2024, 1, 1),
                    900,
                    2.0,
                    "DEBUG",
                    [],
                    "",
                )
                simulation_id = simulation_inventory.add_simulation(simulation)
                simulation_inventory.add_models_to_simulation(simulation_id, [model])

                # Act
                pod_name = simulation_inventory.get_models_from_simulation(
                    simulation_id
                )[0].pod_name

                # Assert
                self.assertTrue(
                    all(c.islower() or c.isdigit() or c == "-" for c in pod_name),
                    f"Pod name '{pod_name}' contains invalid characters.",
                )
                self.assertTrue(
                    pod_name[0].isalnum() and pod_name[-1].isalnum(),
                    f"Pod name '{pod_name}' must start and end with an alphanumeric character.",
                )
                self.assertLessEqual(
                    len(pod_name),
                    63,
                    f"Pod name '{pod_name}' exceeds the maximum length of 63 characters.",
                )


if __name__ == "__main__":
    unittest.main()
