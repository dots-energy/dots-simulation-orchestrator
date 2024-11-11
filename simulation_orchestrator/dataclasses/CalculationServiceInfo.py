from dataclasses import dataclass
from typing import List

from simulation_orchestrator.rest.schemas.EnvironmentVariable import EnvironmentVariable
from simulation_orchestrator.types import EsdlId

@dataclass
class CalculationServiceInfo:
    calc_service_name : str
    service_image_url : str
    nr_of_models : int
    amount_of_calculations : int
    esdl_type : str
    esdl_ids : List[EsdlId]
    additional_environment_variables : List[EnvironmentVariable]