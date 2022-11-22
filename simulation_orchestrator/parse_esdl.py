from typing import List

from esdl import esdl, EnergySystem
from esdl.esdl_handler import EnergySystemHandler
from base64 import b64decode

from simulation_orchestrator.models.model_inventory import Model
from simulation_orchestrator.types import ProgressState


def get_energy_system(esdl_base64string: str) -> EnergySystem:
    esdl_string = b64decode(esdl_base64string + b"==".decode("utf-8")).decode("utf-8")

    esh = EnergySystemHandler()
    esh.load_from_string(esdl_string)
    return esh.get_energy_system()


def get_model_list(calculation_services: List[dict], esdl_base64string: str) -> List[Model]:
    energy_system = get_energy_system(esdl_base64string)

    model_list: List[Model] = []
    # Iterate over all contents of an EnergySystem
    for esdl_obj in energy_system.eAllContents():
        add_model(model_list, calculation_services, esdl_obj)

    if next((True for calc_service in calculation_services if
             calc_service["esdl_type"] == esdl.EnergySystem.__name__), False):
        add_model(model_list, calculation_services, energy_system)

    return model_list


def add_model(model_list: List[Model], calculation_services: List[dict], esdl_obj: esdl):
    calc_service = next(
        (
            calc_service
            for calc_service in calculation_services
            if calc_service["esdl_type"] == type(esdl_obj).__name__
        ),
        None,
    )

    if calc_service:
        model_id = f"{esdl_obj.name.lower().replace(' ', '-')[:20]}-{str(esdl_obj.id).lower()[:8]}"
        model_list.append(
            Model(
                model_id=model_id,
                model_name=esdl_obj.name,
                esdl_uuid=esdl_obj.id,
                calc_service_name=calc_service['calc_service_name'],
                service_image_url=calc_service['service_image_url'],
                current_state=ProgressState.REGISTERED,
            )
        )
