from fastapi import APIRouter

from simulation_orchestrator.rest.api.api_v1.endpoints import simulation_api


api_router = APIRouter()
api_router.include_router(
    simulation_api.router, prefix="/simulation", tags=["simulation"]
)
