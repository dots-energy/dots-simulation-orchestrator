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


def get_models_list(calculation_services: List[dict], esdl_base64string: str) -> List[Model]:
    energy_system = get_energy_system(esdl_base64string)

    models_list = []
    # Iterate over all contents of an EnergySystem
    for asset in energy_system.eAllContents():
        calc_service = next(
            (
                calc_service
                for calc_service in calculation_services
                if calc_service["esdl_type"] == type(asset).__name__
            ),
            None,
        )

        # print(f"{type(asset).__name__}, {calc_service}")

        if calc_service:
            models_list.append(
                Model(
                    model_id=asset.id,
                    model_name=asset.name,
                    calc_service_name=calc_service['calc_service_name'],
                    service_image_url=calc_service['service_image_url'],
                    current_state=ProgressState.REGISTERED,
                )
            )
        # elif isinstance(asset, esdl.EnergyAsset):  # all energy assets should have a calculation service (for now)
        #     print(
        #         f"No Calculation Service found for ESDL Asset Type: {type(asset).__name__}"
        #     )

    return models_list
