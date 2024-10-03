from typing import Sequence
from pydantic import BaseModel
from simulation_orchestrator.rest.schemas.SimulationStatus import SimulationStatus


class SimulationList(BaseModel):
    simulations: Sequence[SimulationStatus]
