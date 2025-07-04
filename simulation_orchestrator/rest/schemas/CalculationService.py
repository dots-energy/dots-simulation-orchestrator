from pydantic import BaseModel, Field

from simulation_orchestrator.rest.schemas.EnvironmentVariable import EnvironmentVariable


class CalculationService(BaseModel):
    esdl_type: str = Field(
        default="PVInstallation", description="The exactname of the ESDL type"
    )
    calc_service_name: str = Field(
        default="pvinstallation_service",
        description="Name of the calculation service,"
        " as described in the code generator yaml config file",
    )
    service_image_url: str = Field(
        default="<pvinstallation_service_docker_image_url>",
        description="The URL of the docker image file",
    )
    nr_of_models: int = Field(
        default=1, description="'0' will create a model (container) per ESDL object"
    )
    amount_of_calculations: int = Field(
        default=1,
        description="Amount of calculations executed by the calculation service",
    )
    additional_env_variable: list[EnvironmentVariable] = Field(
        default=[], description="A"
    )
