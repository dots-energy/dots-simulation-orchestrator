# ruff: noqa: F821

from io import BytesIO
import json
from pathlib import Path
import typing
from zipfile import BadZipFile

import esdl
from fastapi import UploadFile
from pydantic import ValidationError
from fmpy.validation import validate_fmu
from fmpy.model_description import ModelDescription, read_model_description

from simulation_orchestrator.data_handler.data_handler import DataHandler
from simulation_orchestrator.rest.schemas.FmuSimulationStatus import FmuSimulationStatus
from simulation_orchestrator.rest.schemas.SimulationPost import SimulationPost
from simulation_orchestrator import parse_esdl
from simulation_orchestrator.simulation_logic.model_inventory import Model
from simulation_orchestrator.simulation_logic.simulation_inventory import (
    SimulationInventory,
    Simulation,
)
from simulation_orchestrator.simulation_logic.simulation_executor import (
    SimulationExecutor,
)

from simulation_orchestrator.types import ProgressState, SimulationId

simulation_inventory: SimulationInventory
simulation_executor: SimulationExecutor
data_handler: DataHandler


def create_new_simulation(simulation_post: SimulationPost) -> Simulation:
    # check if esdl is readable
    parse_esdl.get_energy_system(simulation_post.esdl_base64string)

    simulator_id = "SO"

    new_simulation = Simulation(
        simulator_id=simulator_id,
        simulation_name=simulation_post.name,
        simulation_start_date=simulation_post.start_date,
        simulation_duration_in_seconds=simulation_post.simulation_duration_in_seconds,
        keep_logs_hours=simulation_post.keep_logs_hours,
        log_level=simulation_post.log_level,
        calculation_services=simulation_post.calculation_services,
        esdl_base64string=simulation_post.esdl_base64string,
    )

    return new_simulation


def start_new_simulation(simulation_post: SimulationPost) -> SimulationId:
    new_simulation = create_new_simulation(simulation_post)

    model_list = parse_esdl.get_model_list(
        new_simulation.calculation_services, new_simulation.esdl_base64string
    )

    simulation_id = simulation_inventory.add_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(
        new_simulation.simulation_id, model_list
    )
    simulation_executor.deploy_simulation(
        simulation_inventory.get_simulation(simulation_id)
    )

    return simulation_id


def queue_new_simulation(simulation_post: SimulationPost) -> SimulationId:
    new_simulation = create_new_simulation(simulation_post)
    model_list = parse_esdl.get_model_list(
        new_simulation.calculation_services, new_simulation.esdl_base64string
    )
    simulation_id = simulation_inventory.queue_simulation(new_simulation)
    simulation_inventory.add_models_to_simulation(
        new_simulation.simulation_id, model_list
    )
    if simulation_inventory.nr_of_queued_simulations() == 1:
        simulation_executor.deploy_simulation(
            simulation_inventory.get_simulation(simulation_id)
        )
    return simulation_id


def get_simulation_and_status(
    simulation_id: SimulationId,
) -> typing.Tuple[typing.Union[Simulation, None], str]:
    return (
        simulation_inventory.get_simulation(simulation_id),
        simulation_inventory.get_status_description(simulation_id),
    )


def get_simulation_and_status_list() -> typing.List[
    typing.Tuple[typing.Union[Simulation, None], str]
]:
    simulation_ids = simulation_inventory.get_simulation_ids()
    return [
        get_simulation_and_status(simulation_id) for simulation_id in simulation_ids
    ]


def terminate_simulation(
    simulation_id: SimulationId,
) -> typing.Tuple[typing.Union[Simulation, None], str]:
    simulation = simulation_inventory.get_simulation(simulation_id)
    if simulation is not None:
        simulation_executor.terminate_simulation(simulation_id)
    return simulation


def delete_pods(simulation_id: SimulationId):
    simulation = simulation_inventory.get_simulation(simulation_id)
    if simulation is not None:
        state = simulation_inventory.get_simulation_state(simulation_id)
        if (
            state == ProgressState.TERMINATED_FAILED
            or ProgressState.TERMINATED_SUCCESSFULL
        ):
            simulation_executor.delete_all_pods_from_simulation(simulation)
    return simulation


def get_all_logs_for_simulation_id(simulation_id: SimulationId) -> BytesIO | None:
    simulation = simulation_inventory.get_simulation(simulation_id)
    if simulation is not None:
        return simulation_executor.get_all_logs_from_simulation(simulation)
    return None


def get_all_data_for_simulation_id(simulation_id: SimulationId) -> BytesIO:
    return data_handler.get_all_data_for_simulation_id(simulation_id)


def _validate_uploaded_files(
    files: typing.List[UploadFile], fmu_files: typing.List[UploadFile]
) -> tuple[str, UploadFile | None]:
    json_file: UploadFile | None = None
    for file in files:
        filename = file.filename.lower()

        if filename.endswith(".json") and json_file is None:
            json_file = file
        elif filename.endswith(".fmu"):
            fmu_files.append(file)
        else:
            return (
                f"Invalid file type: {file.filename}. Only ONE .json and .fmu are allowed.",
                None,
            )

    if json_file is None:
        return (
            "No JSON file uploaded. Please upload one .json file with the simulation configuration.",
            None,
        )

    if len(fmu_files) == 0:
        return "No FMU files uploaded. Please upload at least one .fmu file.", None

    return "", json_file


def _validate_simulation_json(
    json_file: UploadFile,
) -> tuple[str, SimulationPost | None]:
    try:
        simulation_post_val = SimulationPost.model_validate(
            json.loads(json_file.file.read())
        )
    except json.JSONDecodeError as e:
        return f"Invalid JSON file: {e}", None
    except ValidationError as e:
        return f"JSON does not conform to SimulationPost schema: {e}", None

    return "", simulation_post_val


def _validate_uploaded_fmus(
    fmu_files: typing.List[UploadFile],
    simulation_id: str,
    model_descriptions: dict[str, ModelDescription],
) -> str:
    ret_val = ""
    file_problems_dict = {}
    for fmu_file in fmu_files:
        upload_dir: Path = Path(__file__).parent / "uploaded_fmus" / simulation_id
        upload_dir.mkdir(parents=True, exist_ok=True)

        path: Path = upload_dir / fmu_file.filename
        problems = []
        with open(path, "wb") as f:
            f.write(fmu_file.file.read())

        try:
            problems.extend(validate_fmu(str(path)))
        except BadZipFile as e:
            problems.append(f"File {fmu_file.filename} is not a valid zip file: {e}")

        if len(problems) > 0:
            file_problems_dict[fmu_file.filename] = problems
        else:
            model_descriptions[fmu_file.filename] = read_model_description(str(path))
        path.unlink()
        upload_dir.rmdir()

    if len(file_problems_dict) > 0:
        ret_val = json.dumps(file_problems_dict)

    return ret_val


def _esdl_obj_descriptions_contains_all_parameter_values(
    description: str, fmu_model: ModelDescription
) -> bool:
    parameters = json.loads(description)
    fmu_model_parameters_names = [
        var.name for var in fmu_model.modelVariables if var.causality == "parameter"
    ]
    return all(
        parameter_name in parameters for parameter_name in fmu_model_parameters_names
    )


def _validate_all_fmu_models_have_valid_parameters(
    fmu_model_descriptions: dict[str, ModelDescription],
    models: typing.List[Model],
    esdl_id_obj_mapping: dict[str, esdl.Asset],
) -> str:
    fmu_models = [model for model in models if len(model.required_fmus) > 0]

    for fmu_model in fmu_models:
        for esdl_id in fmu_model.esdl_ids:
            esdl_obj = esdl_id_obj_mapping[esdl_id]
            if not hasattr(esdl_obj, "description") or not hasattr(esdl_obj, "name"):
                return f"ESDL object with id {esdl_id} does not have required attributes 'name' and 'description'"
            elif esdl_obj.name not in fmu_model_descriptions:
                return f"ESDL object with id {esdl_id} has name {esdl_obj.name} which does not match any of the uploaded FMU model names"
            elif not _esdl_obj_descriptions_contains_all_parameter_values(
                esdl_obj.description, fmu_model_descriptions[esdl_obj.name]
            ):
                return f"ESDL object with id {esdl_id} has description which does not contain all parameter values required by the FMU model {esdl_obj.name}"

    return ""


def add_fmu_simulation(files: typing.List[UploadFile]) -> FmuSimulationStatus:
    fmu_files: typing.List[UploadFile] = []

    error_msg, json_file = _validate_uploaded_files(files, fmu_files)
    if error_msg != "":
        return FmuSimulationStatus(True, error_msg, None)

    error_msg, simulation_post = _validate_simulation_json(json_file)
    if error_msg != "":
        return FmuSimulationStatus(True, error_msg, None)

    simulation_id = simulation_inventory.add_simulation(
        create_new_simulation(simulation_post)
    )

    model_descriptions: dict[str, ModelDescription] = {}
    error_msg = _validate_uploaded_fmus(fmu_files, simulation_id, model_descriptions)
    if error_msg != "":
        simulation_inventory.remove_simulation(simulation_id)
        return FmuSimulationStatus(True, error_msg, None)

    new_simulation = create_new_simulation(simulation_post)

    esdl_id_obj_mapping: dict[str, esdl.Asset] = {}
    model_list = parse_esdl.get_model_list(
        new_simulation.calculation_services,
        new_simulation.esdl_base64string,
        esdl_id_obj_mapping,
    )

    error_msg = _validate_all_fmu_models_have_valid_parameters(
        model_descriptions, model_list, esdl_id_obj_mapping
    )
    if error_msg != "":
        simulation_inventory.remove_simulation(simulation_id)
        return FmuSimulationStatus(True, error_msg, None)

    simulation_inventory.add_models_to_simulation(
        new_simulation.simulation_id, model_list
    )

    return FmuSimulationStatus(False, "", simulation_id)
