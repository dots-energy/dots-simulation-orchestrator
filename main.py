#!/usr/bin/env python
import os
import typing
import simulation_orchestrator.actions as actions
import uvicorn

from dotenv import load_dotenv
from simulation_orchestrator.io.log import LOGGER
from simulation_orchestrator.simulation_logic.simulation_inventory import (
    SimulationInventory,
)
from simulation_orchestrator.data_handler.data_handler import DataHandler
from simulation_orchestrator.model_services_orchestrator.k8s_api import K8sApi
from simulation_orchestrator.simulation_logic.simulation_executor import (
    SimulationExecutor,
)
from starlette.templating import _TemplateResponse

from dots_infrastructure.influxdb_connector import InfluxDBConnector

from pathlib import Path
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from simulation_orchestrator.rest.api.api_v1.api import api_router
import simulation_orchestrator.rest.oauth.OAuthUtilities
from simulation_orchestrator.rest.core.config import settings

load_dotenv()  # take environment variables from .env

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "rest/templates/"))

root_router = APIRouter()
app = FastAPI(title="DOTS Simulation Orchestrator API")
app.mount(
    "/rest/images/",
    StaticFiles(directory=str(BASE_PATH / "rest/images/")),
    name="images",
)


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
    CONFIG_KEYS = [
        ("INFLUXDB_HOST", "", str, False),
        ("INFLUXDB_PORT", "", str, False),
        ("INFLUXDB_USER", "", str, False),
        ("INFLUXDB_PASSWORD", "", str, True),
        ("INFLUXDB_NAME", "", str, False),
        ("SECRET_KEY", None, str, True),
        ("OAUTH_PASSWORD", None, str, True),
    ]

    @staticmethod
    def load(
        keys: typing.List[typing.Tuple[str, typing.Optional[str], typing.Any, bool]],
    ) -> typing.Dict[str, typing.Any]:
        result = {}
        LOGGER.info("Config:")
        max_length_name = max(len(key[0]) for key in keys)
        for name, default, transform, hide in keys:
            if default is None and (name not in os.environ):
                raise Exception(f"Missing environment variable {name}")

            env_value = os.getenv(name, default)
            LOGGER.info(
                f"    {f'{name}:'.ljust(max_length_name + 4)}{'<hidden>' if hide else env_value}"
            )
            result[name] = transform(env_value)
        LOGGER.info("")

        return result


def start():
    env_config = EnvConfig.load(EnvConfig.CONFIG_KEYS)

    simulation_inventory = SimulationInventory()
    generic_model_env_var: dict = {}
    for key, value in env_config.items():
        if key.startswith("INFLUXDB"):
            generic_model_env_var[key] = value

    simulation_orchestrator.rest.oauth.OAuthUtilities.SECRET_KEY = env_config[
        "SECRET_KEY"
    ]
    simulation_orchestrator.rest.oauth.OAuthUtilities.users["DotsUser"][
        "hashed_password"
    ] = simulation_orchestrator.rest.oauth.OAuthUtilities.get_password_hash(
        env_config["OAUTH_PASSWORD"]
    )

    actions.simulation_inventory = simulation_inventory
    actions.simulation_executor = SimulationExecutor(
        K8sApi(generic_model_env_var), simulation_inventory
    )

    influxdb_client: InfluxDBConnector = InfluxDBConnector(
        env_config["INFLUXDB_HOST"],
        env_config["INFLUXDB_PORT"],
        env_config["INFLUXDB_USER"],
        env_config["INFLUXDB_PASSWORD"],
        env_config["INFLUXDB_NAME"],
    )
    actions.data_handler = DataHandler(influxdb_client)
    influxdb_client.create_database()

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")


if __name__ == "__main__":
    start()
