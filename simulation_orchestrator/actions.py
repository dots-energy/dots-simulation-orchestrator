from io import BytesIO
import typing

from simulation_orchestrator.data_handler.data_handler import DataHandler
from simulation_orchestrator.rest.schemas.SimulationPost import SimulationPost
from simulation_orchestrator import parse_esdl
from simulation_orchestrator.simulation_logic.simulation_inventory import SimulationInventory, Simulation
from simulation_orchestrator.simulation_logic.simulation_executor import SimulationExecutor

from simulation_orchestrator.types import ProgressState, SimulationId

simulation_inventory: SimulationInventory
simulation_executor: SimulationExecutor
data_handler: DataHandler

def create_new_simulation(simulation_post : SimulationPost) -> Simulation:
    
    # check if esdl is readable
    parse_esdl.get_energy_system(simulation_post.esdl_base64string)

    simulator_id = 'SO'

    new_simulation = Simulation(
        simulator_id=simulator_id,
        simulation_name=simulation_post.name,
        simulation_start_date=simulation_post.start_date,
        simulation_duration_in_seconds=simulation_post.simulation_duration_in_seconds,
        keep_logs_hours=simulation_post.keep_logs_hours,
        log_level=simulation_post.log_level,
        calculation_services=simulation_post.calculation_services,
        esdl_base64string=simulation_post.esdl_base64string
    )

    return new_simulation

def start_new_simulation(simulation_post: SimulationPost) -> SimulationId:

    new_simulation = create_new_simulation(simulation_post)

    model_list = parse_esdl.get_model_list(new_simulation.calculation_services, new_simulation.esdl_base64string)

    simulation_id = simulation_inventory.add_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(new_simulation.simulation_id, model_list)
    simulation_executor.deploy_simulation(simulation_inventory.get_simulation(simulation_id))

    return simulation_id

def queue_new_simulation(simulation_post: SimulationPost) -> SimulationId:
    new_simulation = create_new_simulation(simulation_post)
    model_list = parse_esdl.get_model_list(new_simulation.calculation_services, new_simulation.esdl_base64string)
    simulation_id = simulation_inventory.queue_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(new_simulation.simulation_id, model_list)
    if simulation_inventory.nr_of_queued_simulations() == 1:
        simulation_executor.deploy_simulation(simulation_inventory.get_simulation(simulation_id))
    return simulation_id

def get_simulation_and_status(simulation_id: SimulationId) -> typing.Tuple[typing.Union[Simulation, None], str]:
    return (
        simulation_inventory.get_simulation(simulation_id),
        simulation_inventory.get_status_description(simulation_id)
    )

def get_simulation_and_status_list() -> typing.List[typing.Tuple[typing.Union[Simulation, None], str]]:
    simulation_ids = simulation_inventory.get_simulation_ids()
    return [
        get_simulation_and_status(simulation_id)
        for simulation_id in simulation_ids
    ]

def terminate_simulation(simulation_id: SimulationId) -> typing.Tuple[typing.Union[Simulation, None], str]:
    simulation = simulation_inventory.get_simulation(simulation_id)
    if simulation != None:
        simulation_executor.terminate_simulation(simulation_id)
    return simulation

def delete_pods(simulation_id : SimulationId):
    simulation = simulation_inventory.get_simulation(simulation_id)
    if simulation != None:
        state = simulation_inventory.get_simulation_state(simulation_id)
        if state == ProgressState.TERMINATED_FAILED or ProgressState.TERMINATED_SUCCESSFULL:
            simulation_executor.delete_all_pods_from_simulation(simulation)
    return simulation

def get_all_data_for_simulation_id(simulation_id: SimulationId) -> BytesIO:
    return data_handler.get_all_data_for_simulation_id(simulation_id)