import typing
from unittest.mock import MagicMock
from simulation_orchestrator.types import ModelId, SimulationId, SimulatorId


class K8sApi:

    def __init__(self):
        self.deploy_new_pod = MagicMock()
        self.await_pod_to_running_state = MagicMock()
        self.deploy_helics_broker = MagicMock()
        self.deploy_model = MagicMock()
        self.delete_pod_with_model_id = MagicMock()
        self.delete_broker_pod_of_simulation_id = MagicMock()
        self.list_pods_status_per_simulation_id = MagicMock()
        self.add_delete_date_to_pods_status_for_simulation_id = MagicMock()

    @staticmethod
    def model_to_pod_name(simulator_id: SimulatorId, simulation_id: SimulationId, model_id: ModelId):
        return f'{simulator_id.lower()}-{simulation_id.lower()}-{model_id.lower()}'
