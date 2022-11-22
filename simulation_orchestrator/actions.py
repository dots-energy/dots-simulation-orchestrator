import typing

from simulation_orchestrator import parse_esdl
from simulation_orchestrator.io.mqtt_broker import MqttBroker
from simulation_orchestrator.models.simulation_inventory import SimulationInventory, Simulation

from simulation_orchestrator.types import SimulationId, ProgressState

simulation_inventory: SimulationInventory
mqtt_broker: MqttBroker


def start_new_simulation(new_simulation: Simulation) -> SimulationId:
    try:
        model_list = parse_esdl.get_model_list(new_simulation.calculation_services, new_simulation.esdl_base64string)
    except Exception as ex:
        raise IOError(f"The ESDL Base64 Encoded string could not be read: {ex},"
                      f"input Base64 string: {new_simulation.esdl_base64string}")

    simulation_id = simulation_inventory.add_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(new_simulation.simulation_id, model_list)
    mqtt_broker.send_deploy_models(new_simulation.simulator_id, new_simulation.simulation_id,
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
    mqtt_broker.send_simulation_done(simulation_id)
    simulation_inventory.set_state_for_all_models(simulation_id, ProgressState.TERMINATED_FAILED)
    return (
        simulation_inventory.get_simulation(simulation_id),
        simulation_inventory.get_status_description(simulation_id)
    )
