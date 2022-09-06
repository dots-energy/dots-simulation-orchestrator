import typing

from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.models.model_inventory import ModelInventory, Model
from simulation_orchestrator.types import SimulationId, EssimId, ModelId, ProgressState, progress_state_description


class Simulation:
    essim_id: EssimId
    simulation_id: SimulationId
    sim_time_start: int
    sim_time_increment: int
    sim_nr_of_time_steps: int

    current_time_step: int
    model_inventory: ModelInventory

    def __init__(self,
                 essim_id: EssimId,
                 simulation_id: SimulationId,
                 sim_time_start: int,
                 sim_time_increment: int,
                 sim_nr_of_steps):
        self.essim_id = essim_id
        self.simulation_id = simulation_id
        self.sim_time_start = sim_time_start
        self.sim_time_increment = sim_time_increment
        self.sim_nr_of_time_steps = sim_nr_of_steps

        self.current_time_step = 0
        self.model_inventory = ModelInventory()


class SimulationInventory:
    activeSimulations: typing.Dict[SimulationId, Simulation]

    def __init__(self):
        self.activeSimulations = {}

    def add_simulation(self, new_simulation: Simulation):
        self.activeSimulations.update({new_simulation.simulation_id: new_simulation})

    def remove_simulation(self, simulation_id: SimulationId):
        LOGGER.info(f'Removing simulation {simulation_id} from inventory')
        popped = self.activeSimulations.pop(simulation_id)

        if not popped:
            LOGGER.warning(f'Simulation {simulation_id} was unknown. This should not happen.')

    def add_models_to_simulation(self, simulation_id: SimulationId, new_models: typing.List[Model]):
        self.activeSimulations.get(simulation_id).model_inventory.add_models_to_simulation(simulation_id,
                                                                                           new_models)

    def get_models_from_simulation(self, simulation_id: SimulationId) -> typing.List[Model]:
        return list(self.activeSimulations.get(simulation_id).model_inventory.get_models())

    def get_model_from_simulation(self, simulation_id: SimulationId, model_id: ModelId) -> typing.Optional[Model]:
        return self.activeSimulations.get(simulation_id).model_inventory.get_model(model_id)

    def get_all_models(self, simulation_id: SimulationId) -> typing.List[Model]:
        return self.activeSimulations.get(simulation_id).model_inventory.get_models()

    def get_model(self, simulation_id: SimulationId, model_id: ModelId) -> Model:
        return self.activeSimulations.get(simulation_id).model_inventory.get_model(model_id)

    def update_model_state_and_get_simulation_state(self, simulation_id: SimulationId, model_id: ModelId,
                                                    new_state: ProgressState) -> ProgressState:
        model = self.activeSimulations.get(simulation_id).model_inventory.get_model(model_id)
        if model:
            old_state = model.current_state
            model.current_state = new_state
            LOGGER.debug(f'Notifying state observers that model {simulation_id}/{model_id} has changed '
                         f'state from {old_state} to {new_state}')
        else:
            LOGGER.warning(f'Model {model_id} in simulation {simulation_id} does not exist so it could not be marked '
                           f'as {new_state}')

        simulation_state = self.get_simulation_state(simulation_id)
        if new_state == ProgressState.TERMINATED_FAILED:
            LOGGER.error(f'Model {model_id} in simulation {simulation_id} does not exist so it could not be marked '
                         f'as {new_state}')
            # TODO remove simulation and clean-up MSO by message? Or do after SIM status request, so proper message can be given?
        return simulation_state

    def _are_all_models_in_state(self, simulation_id, state: ProgressState) -> bool:
        return all(model.current_state == state for model in self.get_all_models(simulation_id))

    def get_simulation_state(self, simulation_id: SimulationId) -> ProgressState:
        model_states = [model.current_state for model in self.get_all_models(simulation_id)]

        min_model_state = min(model_states)
        max_model_state = max(model_states)
        if max_model_state - min_model_state > 1 and min_model_state != ProgressState.TERMINATED_FAILED:
            LOGGER.warning(f"Both model states '{progress_state_description[min_model_state]}' and "
                           f"'{progress_state_description[max_model_state]}' are present in the simulation"
                           f"which should not happen.")

        return min_model_state

    def set_status_for_all_models(self, simulation_id: SimulationId, new_state: ProgressState):
        for model in self.get_all_models(simulation_id):
            model.current_state = new_state

    def increment_time_step_and_get_timestamp(self, simulation_id: SimulationId) -> int:
        simulation = self.activeSimulations.get(simulation_id)
        simulation.current_time_step += 1
        LOGGER.info(
            f'Starting calculation step {simulation.current_time_step} (of {simulation.sim_nr_of_time_steps})')
        return simulation.sim_time_start + simulation.sim_time_increment * simulation.current_time_step

    def on_last_time_step(self, simulation_id: SimulationId) -> bool:
        simulation = self.activeSimulations.get(simulation_id)
        return simulation.current_time_step == simulation.sim_nr_of_time_steps

    def get_status_description(self, simulation_id: SimulationId) -> str:
        if self.get_simulation_state(simulation_id) == ProgressState.STEP_STARTED:
            simulation = self.activeSimulations.get(simulation_id)
            return f"Calculating time step {simulation.current_time_step} (of {simulation.sim_nr_of_time_steps})"
