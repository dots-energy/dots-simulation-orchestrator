import math
from typing import List

from esdl import esdl, EnergySystem
from esdl.esdl_handler import EnergySystemHandler
from base64 import b64decode

from simulation_orchestrator.rest.schemas.CalculationService import CalculationService
from simulation_orchestrator.dataclasses.CalculationServiceInfo import (
    CalculationServiceInfo,
)
from simulation_orchestrator.simulation_logic.model_inventory import Model
from simulation_orchestrator.types import ProgressState


def get_energy_system(esdl_base64string: str) -> EnergySystem:
    esdl_string = b64decode(esdl_base64string + b"==".decode("utf-8")).decode("utf-8")

    esh = EnergySystemHandler()
    esh.load_from_string(esdl_string)
    return esh.get_energy_system()


def extract_calculation_service(
    calculation_services: List[CalculationService], esdl_obj
) -> CalculationService:
    esdl_obj_type_name = type(esdl_obj).__name__
    calc_service = next(
        (
            calc_service
            for calc_service in calculation_services
            if calc_service.esdl_type == esdl_obj_type_name
        ),
        None,
    )

    return calc_service


def add_esdl_object(
    service_info_dict: dict[str, CalculationServiceInfo],
    calculation_services: List[CalculationService],
    esdl_obj: esdl,
):
    calc_service = extract_calculation_service(calculation_services, esdl_obj)

    if calc_service:
        if calc_service.calc_service_name in service_info_dict:
            service_info_dict[calc_service.calc_service_name].esdl_ids.append(
                esdl_obj.id
            )
        else:
            service_info_dict[calc_service.calc_service_name] = CalculationServiceInfo(
                calc_service.calc_service_name,
                calc_service.service_image_url,
                calc_service.nr_of_models,
                calc_service.amount_of_calculations,
                type(esdl_obj).__name__,
                [esdl_obj.id],
                calc_service.additional_env_variable,
            )


def get_model_list(
    calculation_services: List[CalculationService], esdl_base64string: str
) -> List[Model]:
    try:
        energy_system = get_energy_system(esdl_base64string)

        # gather all esdl objects per calculation service
        service_info_dict: dict[str, CalculationServiceInfo] = {}
        # Iterate over all contents of an EnergySystem
        for esdl_obj in energy_system.eAllContents():
            add_esdl_object(service_info_dict, calculation_services, esdl_obj)

        if next(
            (
                True
                for calc_service in calculation_services
                if calc_service.esdl_type == esdl.EnergySystem.__name__
            ),
            False,
        ):
            add_esdl_object(service_info_dict, calculation_services, energy_system)

        # create model(s) per calculation service
        model_list: List[Model] = []
        for service_info in service_info_dict.values():
            add_service_models(service_info, model_list)
    except Exception as ex:
        raise IOError(f"Error getting Model list from ESDL: {ex},")

    return model_list


def add_service_models(service_info: CalculationServiceInfo, model_list):
    nr_of_esdl_objects = len(service_info.esdl_ids)
    if service_info.nr_of_models == 0:
        nr_of_objects_in_model = 1
    else:
        nr_of_objects_in_model = math.ceil(
            nr_of_esdl_objects / service_info.nr_of_models
        )

    i_model = 0
    while i_model * nr_of_objects_in_model < nr_of_esdl_objects:
        i_model += 1
        model_id = f"{service_info.calc_service_name.replace('_', '-')}-{i_model}"

        esdl_ids = []
        for i_esdl_id in range(
            (i_model - 1) * nr_of_objects_in_model, i_model * nr_of_objects_in_model
        ):
            if i_esdl_id < len(service_info.esdl_ids):
                esdl_ids.append(service_info.esdl_ids[i_esdl_id])

        model_list.append(
            Model(
                model_id=model_id,
                esdl_ids=esdl_ids,
                calc_service=service_info,
                current_state=ProgressState.REGISTERED,
            )
        )
