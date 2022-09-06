import typing

from simulation_orchestrator.io.mqtt_broker import MqttBroker
from simulation_orchestrator.models.model_inventory import Model
from simulation_orchestrator.models.simulation_inventory import SimulationInventory, Simulation
from simulation_orchestrator.types import ProgressState

simulation_inventory: SimulationInventory
mqtt_broker: MqttBroker


def post_request_esdl_file():
    # TODO To be filled from ESDL file
    models_input = [
        {
            'service_name': 'mock_service1',
            'image_url': 'mock_service1:0.0.1',  # local kind image for now
            'model_id': 'mock-service1-12345',
            'model_parameters': {'model_parameter1': 'type_a'},
            'receiving_services': {}
        },
        {
            'service_name': 'mock_service2',
            'image_url': 'mock_service2:0.0.1',
            'model_id': 'mock-service2-12345',
            'model_parameters': {'model_parameter1': '5', 'model_parameter2': '100'},
            'receiving_services': {
                "mock_service1": {"number_of": "1", "model_ids": ["mock-service1-12345"]}
            }
        }
    ]

    # TODO To be filled from EDSL file? Or separate json body?
    log_level = 'DEBUG'
    essim_id = 'essim01'
    simulation_id = 'sim-12345'  # TODO to be created here
    sim_time_start = 0
    sim_time_increment = 3600
    sim_nr_of_time_steps = 3

    model_list: typing.List[Model] = []
    for model_input in models_input:
        model_list.append(
            Model(
                service_name=model_input['service_name'],
                model_id=model_input['model_id'],
                image_url=model_input['image_url'],
                parameters=model_input['model_parameters'],
                receiving_services=model_input['receiving_services'],
                current_state=ProgressState.REGISTERED,
            )
        )

    # On New Simulation (POST request with ESDL file)
    simulation_inventory.add_simulation(
        new_simulation=Simulation(
            essim_id=essim_id,
            simulation_id=simulation_id,
            sim_time_start=sim_time_start,
            sim_time_increment=sim_time_increment,
            sim_nr_of_steps=sim_nr_of_time_steps,
        ))
    simulation_inventory.add_models_to_simulation(simulation_id, model_list)

    mqtt_broker.send_deploy_models(essim_id, simulation_id, log_level)


if __name__ == '__main__':
    post_request_esdl_file()
