from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

import typing
from datetime import timedelta
from simulation_orchestrator.rest.oauth.OAuthUtilities import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

from simulation_orchestrator.rest.schemas.SimulationPost import SimulationPost
from simulation_orchestrator.rest.schemas.SimulationStatus import SimulationStatus
from simulation_orchestrator.rest.schemas.SimulationList import SimulationList
from simulation_orchestrator.rest.schemas.user_schemas import User
from simulation_orchestrator import actions
from simulation_orchestrator.types import ProgressState

router = APIRouter()

@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{simulation_id}", status_code=200, response_model=SimulationStatus)
def get_simulation_status(current_user: Annotated[User, Depends(get_current_user)], *, simulation_id: str ) -> SimulationStatus:
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
def list_simulations(current_user: Annotated[User, Depends(get_current_user)]) -> SimulationList:
    simulation_status_list: typing.List[SimulationStatus] = []
    for simulation, status in actions.get_simulation_and_status_list():
        simulation_status_list.append(
            SimulationStatus.from_simulation_and_status(simulation, status)
        )
    return SimulationList(simulations=simulation_status_list)

@router.post("/start", status_code=201, response_model=SimulationStatus)
def start_new_simulation(current_user: Annotated[User, Depends(get_current_user)], *, simulation_post: SimulationPost ) -> SimulationStatus:

    simulation_id = actions.start_new_simulation(simulation_post)

    simulation_status = SimulationStatus.from_simulation_and_status(*actions.get_simulation_and_status(simulation_id))

    return simulation_status

@router.post("/queue", status_code=201, response_model=SimulationStatus)
def queue_new_simulation(current_user: Annotated[User, Depends(get_current_user)], *, simulation_post: SimulationPost ) -> SimulationStatus:

    simulation_id = actions.queue_new_simulation(simulation_post)

    simulation_status = SimulationStatus.from_simulation_and_status(*actions.get_simulation_and_status(simulation_id))

    return simulation_status


@router.delete("/{simulation_id}", status_code=200, response_model=SimulationStatus)
def terminate_simulation(current_user: Annotated[User, Depends(get_current_user)], *, simulation_id: str ) -> SimulationStatus:
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
