import esdl
from pydantic import ValidationError
from fmpy.validation import validate_fmu
from fmpy.model_description import ModelDescription, read_model_description
from zipfile import BadZipFile
import json
from pathlib import Path
from fastapi import UploadFile
import typing

from simulation_orchestrator.rest.schemas.SimulationPost import SimulationPost
from simulation_orchestrator.simulation_logic.model_inventory import Model


def validate_uploaded_files(
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


def validate_simulation_json(
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


def validate_uploaded_fmus(
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


def esdl_obj_descriptions_contains_all_parameter_values(
    description: str, fmu_model: ModelDescription
) -> bool:
    parameters = json.loads(description)
    fmu_model_parameters_names = [
        var.name for var in fmu_model.modelVariables if var.causality == "parameter"
    ]
    return all(
        parameter_name in parameters for parameter_name in fmu_model_parameters_names
    )


def validate_all_fmu_models_have_valid_parameters(
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
            elif not esdl_obj_descriptions_contains_all_parameter_values(
                esdl_obj.description, fmu_model_descriptions[esdl_obj.name]
            ):
                return f"ESDL object with id {esdl_id} has description which does not contain all parameter values required by the FMU model {esdl_obj.name}"

    return ""
