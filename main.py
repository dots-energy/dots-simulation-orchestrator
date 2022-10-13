#!/usr/bin/env python
import os
from dotenv import load_dotenv
from starlette.templating import _TemplateResponse

load_dotenv()  # take environment variables from .env

import threading
import typing

from simulation_orchestrator.io.mqtt_broker import MqttBroker
from simulation_orchestrator.models.simulation_inventory import SimulationInventory
import simulation_orchestrator.actions as actions
from simulation_orchestrator.io.log import LOGGER

import uvicorn
from pathlib import Path
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates

from rest.api.api_v1.api import api_router
from rest.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "rest/templates"))

root_router = APIRouter()
app = FastAPI(title="DOTS Simulation Orchestrator API")


@root_router.get("/", status_code=200)
def root(request: Request) -> _TemplateResponse:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request},
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


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


def start():
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

    actions.simulation_inventory = simulation_inventory
    actions.mqtt_broker = mqtt_broker

    t = threading.Thread(target=mqtt_broker.start, name='mqtt broker')
    t.daemon = True
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")


if __name__ == '__main__':
    start()
