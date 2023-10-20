from fastapi import APIRouter, HTTPException
import typing

from rest.schemas.simulation_schemas import SimulationPost, SimulationStatus, SimulationList
from simulation_orchestrator import parse_esdl, actions
from simulation_orchestrator.models.simulation_inventory import Simulation
from simulation_orchestrator.types import ProgressState

router = APIRouter()

@router.get("/{simulation_id}", status_code=200, response_model=SimulationStatus)
def get_simulation_status(*, simulation_id: str) -> SimulationStatus:
    """
    Fetch a single simulation by ID
    """
    simulation, status = actions.get_simulation_and_status(simulation_id)
    if not simulation:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Simulation with ID '{simulation_id}' not found"
        )
    return SimulationStatus.from_simulation_and_status(simulation, status)


@router.get("/", status_code=200, response_model=SimulationList)
def list_simulations() -> SimulationList:
    simulation_status_list: typing.List[SimulationStatus] = []
    for simulation, status in actions.get_simulation_and_status_list():
        simulation_status_list.append(
            SimulationStatus.from_simulation_and_status(simulation, status)
        )
    return SimulationList(simulations=simulation_status_list)


@router.post("/start", status_code=201, response_model=SimulationStatus)
def start_new_simulation(*, simulation_post: SimulationPost) -> SimulationStatus:

    simulation_id = actions.start_new_simulation(simulation_post)

    simulation_status = SimulationStatus.from_simulation_and_status(*actions.get_simulation_and_status(simulation_id))

    return simulation_status

@router.post("/queue", status_code=201, response_model=SimulationStatus)
def queue_new_simulation(*, simulation_post: SimulationPost) -> SimulationStatus:

    simulation_id = actions.queue_new_simulation(simulation_post)

    simulation_status = SimulationStatus.from_simulation_and_status(*actions.get_simulation_and_status(simulation_id))

    return simulation_status


@router.delete("/{simulation_id}", status_code=200, response_model=SimulationStatus)
def terminate_simulation(*, simulation_id: str) -> SimulationStatus:
    """
    Terminate a single simulation by ID
    """
    simulation, status = actions.terminate_simulation(simulation_id)
    if not simulation:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Simulation with ID {simulation_id} not found"
        )
    return SimulationStatus.from_simulation_and_status(simulation, str(ProgressState.TERMINATED_FAILED))
