import typing

from simulation_orchestrator.dataclasses.CalculationServiceInfo import (
    CalculationServiceInfo,
)
from simulation_orchestrator.helpers.string_helpers import StringHelpers
from simulation_orchestrator.io.log import LOGGER

from simulation_orchestrator.types import SimulationId, ModelId, ProgressState


class Model:
    model_id: ModelId
    esdl_ids: typing.List[str]
    model_instance: int
    service_image_url: str
    esdl_type: str
    pod_name: str
    current_state: ProgressState

    def __init__(
        self,
        model_id: ModelId,
        model_instance: int,
        esdl_ids: typing.List[str],
        calc_service: CalculationServiceInfo,
        current_state: ProgressState,
    ):
        self.model_id = model_id
        self.model_instance = model_instance
        self.esdl_ids = esdl_ids
        self.calc_service = calc_service
        self.current_state = current_state
        self.pod_name = ""


StateChangeObserver = typing.Callable[
    ["ModelInventory", SimulationId, Model, ProgressState],
    typing.Coroutine[typing.Any, typing.Any, None],
]


class ModelInventory:
    active_models: typing.Dict[ModelId, Model]

    state_observers: typing.List[StateChangeObserver]

    def __init__(self, simulator_id: str):
        self.active_models = {}
        self.state_observers = []
        self.simulator_id: str = simulator_id

    def add_models_to_simulation(
        self, simulation_id: SimulationId, new_models: typing.List[Model]
    ):
        LOGGER.info(
            f"Adding models {[model.model_id for model in new_models]} for simulation {simulation_id} "
            f"to inventory"
        )
        for model in new_models:
            pod_name = f"{self.simulator_id}-{simulation_id}-{model.model_id}"
            pod_name = StringHelpers.sanitize_string(pod_name)
            MAX_LENGTH_POD_NAME = 63
            if len(pod_name) > MAX_LENGTH_POD_NAME:
                amount_of_characters_to_remove = len(pod_name) - MAX_LENGTH_POD_NAME
                model_id_shortened = f"{model.model_id[: -amount_of_characters_to_remove + len(str(model.model_instance))]}{model.model_instance}"
                pod_name = f"{self.simulator_id}-{simulation_id}-{model_id_shortened}"

            model.pod_name = pod_name

        self.active_models.update({model.model_id: model for model in new_models})

    def remove_model(self, simulation_id, model_id):
        LOGGER.info(
            f"Removing model {model_id} from inventory for simulation {simulation_id}"
        )
        popped = self.active_models.pop(model_id)

        if not popped:
            LOGGER.warning(
                f"Model {model_id} for simulation {simulation_id} was unknown. This should not happen."
            )

    def get_models(self) -> typing.List[Model]:
        return list(self.active_models.values())

    def get_model(self, model_id: ModelId) -> typing.Optional[Model]:
        return self.active_models.get(model_id)
