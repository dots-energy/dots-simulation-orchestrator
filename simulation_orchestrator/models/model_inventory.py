import typing

from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.types import SimulationId, ModelId, ProgressState


class Model:
    model_id: ModelId
    model_name: str
    esdl_ids: typing.List[str]
    calc_service_name: str
    service_image_url: str
    current_state: ProgressState

    def __init__(self,
                 model_id: ModelId,
                 esdl_ids: typing.List[str],
                 calc_service_name: str,
                 service_image_url: str,
                 current_state: ProgressState):
        self.model_id = model_id
        self.esdl_ids = esdl_ids
        self.calc_service_name = calc_service_name
        self.service_image_url = service_image_url
        self.current_state = current_state


StateChangeObserver = typing.Callable[['ModelInventory', SimulationId, Model, ProgressState],
                                      typing.Coroutine[typing.Any, typing.Any, None]]


class ModelInventory:
    active_models: typing.Dict[ModelId, Model]

    state_observers: typing.List[StateChangeObserver]

    def __init__(self):
        self.active_models = {}
        self.state_observers = []

    def add_models_to_simulation(self, simulation_id: SimulationId, new_models: typing.List[Model]):
        LOGGER.info(f'Adding models {[model.model_id for model in new_models]} for simulation {simulation_id} '
                    f'to inventory')
        self.active_models.update({model.model_id: model for model in new_models})

    def remove_model(self, simulation_id, model_id):
        LOGGER.info(f'Removing model {model_id} from inventory for simulation {simulation_id}')
        popped = self.active_models.pop(model_id)

        if not popped:
            LOGGER.warning(f'Model {model_id} for simulation {simulation_id} was unknown. This should not happen.')

    def get_models(self) -> typing.List[Model]:
        return list(self.active_models.values())

    def get_model(self, model_id: ModelId) -> typing.Optional[Model]:
        return self.active_models.get(model_id)
