import typing

from rest.schemas.simulation_schemas import SimulationPost
from simulation_orchestrator import parse_esdl
from simulation_orchestrator.io.mqtt_client import MqttClient
from simulation_orchestrator.models.simulation_inventory import SimulationInventory, Simulation

from simulation_orchestrator.types import SimulationId, ProgressState

simulation_inventory: SimulationInventory
mqtt_client: MqttClient

def create_new_simulation(simulation_post : SimulationPost) -> Simulation:
    
    # check if esdl is readable
    parse_esdl.get_energy_system(simulation_post.esdl_base64string)

    simulator_id = 'SO'

    calculation_services = [
        {
            "esdl_type": calculation_service.esdl_type,
            "calc_service_name": calculation_service.calc_service_name,
            "service_image_url": calculation_service.service_image_url,
            "nr_of_models": calculation_service.nr_of_models,
        }
        for calculation_service in simulation_post.calculation_services
    ]

    new_simulation = Simulation(
        simulator_id=simulator_id,
        simulation_name=simulation_post.name,
        simulation_start_date=simulation_post.start_date,
        time_step_seconds=simulation_post.time_step_seconds,
        max_step_calc_time_minutes=simulation_post.max_step_calc_time_minutes,
        sim_nr_of_steps=simulation_post.nr_of_time_steps,
        keep_logs_hours=simulation_post.keep_logs_hours,
        log_level=simulation_post.log_level,
        calculation_services=calculation_services,
        esdl_base64string=simulation_post.esdl_base64string
    )

    return new_simulation

def start_new_simulation(simulation_post: SimulationPost) -> SimulationId:

    new_simulation = create_new_simulation(simulation_post)

    model_list = parse_esdl.get_model_list(new_simulation.calculation_services, new_simulation.esdl_base64string)

    simulation_id = simulation_inventory.add_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(new_simulation.simulation_id, model_list)
    mqtt_client.send_deploy_models(new_simulation.simulator_id, new_simulation.simulation_id,
                                   new_simulation.keep_logs_hours, new_simulation.log_level)

    return simulation_id

def queue_new_simulation(simulation_post: SimulationPost) -> SimulationId:
    new_simulation = create_new_simulation(simulation_post)
    model_list = parse_esdl.get_model_list(new_simulation.calculation_services, new_simulation.esdl_base64string)
    simulation_id = simulation_inventory.queue_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(new_simulation.simulation_id, model_list)
    if simulation_inventory.nr_of_queued_simulations() == 1:
        mqtt_client.send_deploy_models(new_simulation.simulator_id, new_simulation.simulation_id,
                                   new_simulation.keep_logs_hours, new_simulation.log_level)
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
    mqtt_client.send_simulation_done(simulation_id)
    simulation_inventory.set_state_for_all_models(simulation_id, ProgressState.TERMINATED_FAILED)
    return (
        simulation_inventory.get_simulation(simulation_id),
        simulation_inventory.get_status_description(simulation_id)
    )
