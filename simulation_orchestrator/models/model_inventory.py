import typing

from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.types import SimulationId, ModelId, ProgressState


class Model:
    model_id: ModelId
    model_name: str
    calc_service_name: str
    service_image_url: str
    current_state: ProgressState

    def __init__(self,
                 model_id: ModelId,
                 model_name: str,
                 calc_service_name: str,
                 service_image_url: str,
                 current_state: ProgressState):
        self.model_id = model_id
        self.model_name = model_name
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

    # def register_state_change_observer(self, observer: StateChangeObserver) -> None:
    #     self.state_observers.append(observer)
    #
    # async def _notify_state_change_observers(self,
    #                                          simulation_id: SimulationId,
    #                                          model: Model,
    #                                          old_state: ProgressState) -> None:
    #     for observer in self.state_observers:
    #         await observer(self, simulation_id, model, old_state)
    #
    # def set_exit_parameters(self,
    #                         simulation_id: SimulationId,
    #                         model_id: ModelId,
    #                         exit_code: typing.Optional[int],
    #                         exit_reason: typing.Optional[str]):
    #     model = self.get_model(simulation_id, model_id)
    #     assert model
    #     LOGGER.info(f'Model {simulation_id}/{model_id} now has exit code {exit_code} due to: {exit_reason}.')
    #     model.exit_code = exit_code
    #     model.exit_reason = exit_reason
    #
    # async def mark_model_as(self,
    #                         simulation_id: SimulationId,
    #                         model_id: ModelId,
    #                         new_state: ProgressState) -> None:
    #     model = self.get_model(simulation_id, model_id)
    #     if model:
    #         old_state = model.current_state
    #
    #         if old_state != new_state:
    #             model.current_state = new_state
    #             LOGGER.debug(f'Notifying state observers that model {simulation_id}/{model_id} has changed '
    #                          f'state from {old_state} to {new_state}')
    #             await self._notify_state_change_observers(simulation_id, model, old_state)
    #     else:
    #         LOGGER.warning(f'Model {model_id} in simulation {simulation_id} does not exist so it could not be marked '
    #                        f'as {new_state}')
