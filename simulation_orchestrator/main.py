#!/usr/bin/env python
import os
import time
import threading
import typing

from simulation_orchestrator.io.mqtt_broker import MqttBroker
from simulation_orchestrator.models.simulation_inventory import SimulationInventory
import simulation_orchestrator.requests as requests

from simulation_orchestrator.io.log import LOGGER


class EnvConfig:
    CONFIG_KEYS = [('MQTT_HOST', 'localhost', str, False),
                   ('MQTT_PORT', '1883', int, False),
                   ('MQTT_QOS', '0', int, False),
                   ('MQTT_USERNAME', '', str, False),
                   ('MQTT_PASSWORD', '', str, True)]

    @staticmethod
    def load(keys: typing.List[typing.Tuple[str,
                                            typing.Optional[str],
                                            typing.Any,
                                            bool]]
             ) -> typing.Dict[str, typing.Any]:
        result = {}
        LOGGER.info('Config:')
        max_length_name = max(len(key[0]) for key in keys)
        for name, default, transform, hide in keys:
            if default is None and (name not in os.environ):
                raise Exception(f'Missing environment variable {name}')

            env_value = os.getenv(name, default)
            LOGGER.info(f'    {f"{name}:".ljust(max_length_name + 4)}{"<hidden>" if hide else env_value}')
            result[name] = transform(env_value)
        LOGGER.info('')

        return result


def main():
    config = EnvConfig.load(EnvConfig.CONFIG_KEYS)

    simulation_inventory = SimulationInventory()

    mqtt_broker = MqttBroker(
        host=config['MQTT_HOST'],
        port=config['MQTT_PORT'],
        qos=config['MQTT_QOS'],
        username=config['MQTT_USERNAME'],
        password=config['MQTT_PASSWORD'],
        simulation_inventory=simulation_inventory
    )

    requests.simulation_inventory = simulation_inventory
    requests.mqtt_broker = mqtt_broker

    t = threading.Thread(target=mqtt_broker.start, name='mqtt broker')
    t.daemon = True
    t.start()

    time.sleep(1)

    LOGGER.debug("POST Request for testing")
    requests.post_request_esdl_file()

    t.join()


if __name__ == '__main__':
    main()
