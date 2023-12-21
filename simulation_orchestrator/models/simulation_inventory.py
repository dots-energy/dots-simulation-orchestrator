import typing
import uuid
from threading import Lock
from datetime import datetime, timedelta

from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.models.model_inventory import ModelInventory, Model
from simulation_orchestrator.types import SimulationId, SimulatorId, ModelId, ProgressState, progress_state_description


class Simulation:
    simulator_id: SimulatorId
    simulation_id: SimulationId
    simulation_name: str

    simulation_start_datetime: datetime
    time_step_seconds: int
    nr_of_time_steps: int

    max_step_calc_time_minutes: float
    keep_logs_hours: float
    log_level: str

    calculation_services: typing.List[dict]
    esdl_base64string: str

    current_time_step_nr: int
    calculation_start_datetime: datetime
    calculation_end_datetime: typing.Optional[datetime]
    current_step_calculation_start_datetime: typing.Optional[datetime]
    model_inventory: ModelInventory
    error_message: str

    terminated: bool

    lock: Lock

    def __init__(
            self,
            simulator_id: SimulatorId,
            simulation_name: str,
            simulation_start_date: datetime,
            time_step_seconds: int,
            sim_nr_of_steps: int,
            max_step_calc_time_minutes: float,
            keep_logs_hours: float,
            log_level: str,
            calculation_services: typing.List[dict],
            esdl_base64string: str,
    ):
        self.simulator_id = simulator_id
        self.simulation_name = simulation_name
        self.simulation_start_datetime = simulation_start_date
        self.time_step_seconds = time_step_seconds
        self.nr_of_time_steps = sim_nr_of_steps

        self.max_step_calc_time_minutes = max_step_calc_time_minutes
        self.keep_logs_hours = keep_logs_hours
        self.log_level = log_level

        self.calculation_services = calculation_services
        self.esdl_base64string = esdl_base64string

        self.current_time_step_nr = 0
        self.calculation_start_datetime = datetime.now()
        self.calculation_end_datetime = None
        self.current_step_calculation_start_datetime = None
        self.model_inventory = ModelInventory()
        self.error_message = ""
        self.terminated = False

        self.lock = Lock()


class SimulationInventory:
    activeSimulations: typing.Dict[SimulationId, Simulation]
    simulationQueue: list[SimulationId]

    def __init__(self):
        self.activeSimulations = {}
        self.simulationQueue = []
    
    def _generate_new_simulationId(self, simulation_name):
        return f"{simulation_name.lower().replace(' ', '-')[:20]}" \
                                       f"-{str(uuid.uuid4())[:8]}"

    def add_simulation(self, new_simulation: Simulation) -> SimulationId:
        new_simulation.simulation_id = self._generate_new_simulationId(new_simulation.simulation_name)

        self.activeSimulations.update({new_simulation.simulation_id: new_simulation})
        return new_simulation.simulation_id

    def queue_simulation(self, new_simulation: Simulation) -> SimulationId:
        new_simulation.simulation_id = self.add_simulation(new_simulation)
        self.simulationQueue.append(new_simulation.simulation_id)        
        LOGGER.info(f'Queing simulation with id: {new_simulation.simulation_id}')
        return new_simulation.simulation_id 

    def nr_of_queued_simulations(self):
        return len(self.simulationQueue)
    
    def pop_simulation_in_queue(self) -> Simulation:
        return self.simulationQueue.pop(0)
    
    def get_active_simulation_in_queue(self) -> str:
        return self.simulationQueue[0]
    
    def is_active_simulation_from_queue(self, simulation_id) -> Simulation:
        return self.nr_of_queued_simulations() > 0 and self.simulationQueue[0] == simulation_id

    def remove_simulation(self, simulation_id: SimulationId):
        LOGGER.info(f'Removing simulation {simulation_id} from inventory')
        if simulation_id in self.simulationQueue:
            self.simulationQueue.remove(simulation_id)

        popped = self.activeSimulations.pop(simulation_id)

        if not popped:
            LOGGER.warning(f'Simulation {simulation_id} was unknown. This should not happen.')

    def get_simulation_ids(self) -> typing.List[SimulationId]:
        return list(self.activeSimulations.keys())

    def get_simulation(self, simulation_id: SimulationId) -> typing.Union[Simulation, None]:
        return self.activeSimulations.get(simulation_id)

    def add_models_to_simulation(self, simulation_id: SimulationId, new_models: typing.List[Model]):
        self.get_simulation(simulation_id).model_inventory.add_models_to_simulation(simulation_id,
                                                                                           new_models)

    def get_models_from_simulation(self, simulation_id: SimulationId) -> typing.List[Model]:
        return list(self.get_simulation(simulation_id).model_inventory.get_models())

    def get_model_from_simulation(self, simulation_id: SimulationId, model_id: ModelId) -> typing.Optional[Model]:
        return self.get_simulation(simulation_id).model_inventory.get_model(model_id)

    def get_all_models(self, simulation_id: SimulationId) -> typing.List[Model]:
        simulation = self.get_simulation(simulation_id)
        if simulation:
            return simulation.model_inventory.get_models()
        else:
            return []

    def get_model(self, simulation_id: SimulationId, model_id: ModelId) -> Model:
        return self.get_simulation(simulation_id).model_inventory.get_model(model_id)

    def update_model_state_and_get_simulation_state(self, simulation_id: SimulationId, model_id: ModelId,
                                                    new_state: ProgressState) -> ProgressState:
        model = self.get_simulation(simulation_id).model_inventory.get_model(model_id)
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

    def _are_all_models_in_state(self, simulation_id: SimulationId, state: ProgressState) -> bool:
        return all(model.current_state == state for model in self.get_all_models(simulation_id))

    def get_simulation_state(self, simulation_id: SimulationId) -> typing.Optional[ProgressState]:
        model_states = [model.current_state for model in self.get_all_models(simulation_id)]

        if not model_states:
            return None

        min_model_state = min(model_states)
        max_model_state = max(model_states)
        if max_model_state - min_model_state > 1 and min_model_state != ProgressState.TERMINATED_FAILED:
            LOGGER.warning(f"Both model states '{progress_state_description[min_model_state]}' and "
                           f"'{progress_state_description[max_model_state]}' are present in the simulation"
                           f"which should not happen.")

        return min_model_state

    def set_state_for_all_models(self, simulation_id: SimulationId, new_state: ProgressState):
        for model in self.get_all_models(simulation_id):
            model.current_state = new_state

    def increment_time_step_and_get_time_start_end_date_dict(self, simulation_id: SimulationId) -> dict:
        simulation = self.get_simulation(simulation_id)
        simulation.current_time_step_nr += 1
        LOGGER.info(
            f"Starting calculation step {simulation.current_time_step_nr} (of {simulation.nr_of_time_steps})"
            f", for simulation ID: '{simulation_id}'")
        return {
            "time_step_nr": str(simulation.current_time_step_nr),
            "start_time_stamp": (simulation.simulation_start_datetime + timedelta(0, (
                    simulation.current_time_step_nr + 1) * simulation.time_step_seconds)).timestamp()
        }

    def on_last_time_step(self, simulation_id: SimulationId) -> bool:
        simulation = self.get_simulation(simulation_id)
        return simulation.current_time_step_nr == simulation.nr_of_time_steps

    def get_status_description(self, simulation_id: SimulationId) -> str:
        state = self.get_simulation_state(simulation_id)
        if not state:
            return f"Simulation id '{simulation_id}' could not be found."
        if state == ProgressState.STEP_STARTED:
            simulation = self.get_simulation(simulation_id)
            return f"Calculating time step {simulation.current_time_step_nr} (of {simulation.nr_of_time_steps})"
        else:
            return str(state)

    def start_step_calculation_time_counting(self, simulation_id: SimulationId):
        self.get_simulation(simulation_id).current_step_calculation_start_datetime = datetime.now()

    def get_simulation_ids_exceeding_step_calc_time(self) -> typing.List[SimulationId]:
        simulation_ids = []
        for simulation_id, simulation in self.activeSimulations.items():
            if not simulation.terminated and simulation.current_step_calculation_start_datetime:
                if datetime.now() > simulation.current_step_calculation_start_datetime + timedelta(
                        minutes=simulation.max_step_calc_time_minutes):
                    LOGGER.info(
                        f"Exceeded step calculation time for simulation: '{simulation.simulation_name}' - '{simulation_id}'")
                    simulation_ids.append(simulation_id)
        return simulation_ids

    def lock_simulation(self, simulation_id: SimulationId):
        self.get_simulation(simulation_id).lock.acquire()

    def release_simulation(self, simulation_id: SimulationId):
        self.get_simulation(simulation_id).lock.release()
