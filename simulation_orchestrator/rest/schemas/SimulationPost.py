from datetime import datetime
from pydantic import BaseModel, Field
from simulation_orchestrator.rest.schemas.CalculationService import CalculationService

class SimulationPost(BaseModel):
    name: str = 'simulation name'
    start_date: datetime = '2023-01-25 00:00:00'
    simulation_duration_in_seconds: int = '86400'
    keep_logs_hours: float = '24.0'
    log_level: str = Field(default='info', description="Options: 'debug', 'info', 'warning', 'error'")
    calculation_services: list[CalculationService]
    esdl_base64string: str = '<esdl_file_base64encoded_string>'