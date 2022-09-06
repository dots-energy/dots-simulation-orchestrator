#!/usr/bin/env python
import time
import threading
import json
from paho.mqtt.client import Client

import messages

# To be filled from .env?
mqtt_host_local = 'localhost'
mqtt_host_docker = 'host.docker.internal'
mqtt_port = '1883'
mqtt_qos = '0'
mqtt_username = 'essim-mso'
mqtt_password = 'Who Does Not Like Essim!?'

# To be filled from ESDL file
models = [
    {
        'service_name': 'mock_service1',
        'image_url': 'mock_service1:0.0.1',  # local kind image for now
        'model_id': 'mock-service1-12345',
        'model_parameters': {'model_parameter1': 'type_a'},
        'receiving_services_dict': {}
    },
    {
        'service_name': 'mock_service2',
        'image_url': 'mock_service2:0.0.1',
        'model_id': 'mock-service2-12345',
        'model_parameters': {'model_parameter1': '5', 'model_parameter2': '100'},
        'receiving_services_dict': {
            "mock_service1": {"number_of": "1", "model_ids": ["mock-service1-12345"]}
        }
    }
]

# To be filled from EDSL file? Or separate json body?
debug_logging = 'true'
essim_id = 'essim01'
simulation_id = 'sim-12345'
sim_time_start = 0
sim_time_increment = 3600
sim_nr_of_time_steps = 3


def on_connect(client, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    pass


def on_message(client, userdata, msg):
    threading.Thread(target=process_message, args=[msg]).start()


mqtt_client = Client(clean_session=True)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.connect(mqtt_host_local, port=int(mqtt_port))


def test_simulation_orchestrator():
    model_configs = []

    for model in models:
        model_id = model['model_id']
        env_vars = [messages.EnvironmentVariable(name='MQTT_HOST', value=mqtt_host_docker),
                    messages.EnvironmentVariable(name='MQTT_PORT', value=mqtt_port),
                    messages.EnvironmentVariable(name='MQTT_QOS', value=mqtt_qos),
                    messages.EnvironmentVariable(name='ESSIM_ID', value=essim_id),
                    messages.EnvironmentVariable(name='SIMULATION_ID', value=simulation_id),
                    messages.EnvironmentVariable(name='MODEL_ID', value=model_id),
                    messages.EnvironmentVariable(name='MQTT_USERNAME', value=mqtt_username),
                    messages.EnvironmentVariable(name='MQTT_PASSWORD', value=mqtt_password),
                    messages.EnvironmentVariable(name='DEBUG_LOGGING', value=debug_logging)]
        model_configs.append(messages.ModelConfiguration(modelID=model_id,
                                                         containerURL=model['image_url'],
                                                         environmentVariables=env_vars))
        mqtt_client.subscribe(f"/log/model/essim/{model_id}/{simulation_id}")
    message = messages.DeployModels(essimID=essim_id, modelConfigurations=model_configs)
    print('Deploying models')
    print(message)

    send_output(f'/lifecycle/essim/mso/{simulation_id}/DeployModels', message.SerializeToString())

    mqtt_client.subscribe(f"/lifecycle/mso/essim/{simulation_id}/ModelsReady")
    # mqtt_client.subscribe(f"/logging/model/essim/{service_model_id}/{simulation_id}/#")

    mqtt_client.loop_forever()


def process_message(msg):
    topic = msg.topic
    print(" [received] {}: {}".format(topic, msg.payload.decode('utf-8')))

    if topic == f"/lifecycle/mso/essim/{simulation_id}/ModelsReady":
        for model in models:
            # send model parameters
            model_parameters_message = messages.ModelParameters(parameters_dict=json.dumps(model['model_parameters']),
                                                                receiving_services=json.dumps(
                                                                    model['receiving_services_dict']))
            send_output(f"/lifecycle/essim/model/{model['model_id']}/ModelParameters",
                        model_parameters_message.SerializeToString())
        print('Sent ModelParameters to all models')
        time.sleep(2)

        for model in models:
            # the 'lifecycle.step' will be sent by the Simulation Orchestrator at the start of each time step
            new_step_message = messages.NewStep(new_step_dict=json.dumps({'time_stamp': '12345'}))
            send_output(f"/lifecycle/essim/model/{model['model_id']}/NewStep",
                        new_step_message.SerializeToString())
        print('Sent NewStep to all models')

        # end with 'lifecycle.stop'
        # send_output(f"/lifecycle/essim/model/{os.getenv('MODEL_ID')}/stop", b'')


def send_output(topic: str, payload: bytes):
    mqtt_client.publish(topic, payload)


if __name__ == '__main__':
    test_simulation_orchestrator()
