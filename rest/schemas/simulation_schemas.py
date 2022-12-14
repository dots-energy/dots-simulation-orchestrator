import typing

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Sequence

from simulation_orchestrator.models.simulation_inventory import Simulation


class CalculationService(BaseModel):
    esdl_type: str = Field(default='PVInstallation', description="The exactname of the ESDL type")
    calc_service_name: str = Field(default='pvinstallation_service',
                                   description="Name of the calculation service,"
                                               " as described in the code generator yaml config file")
    service_image_url: str = Field(default='<pvinstallation_service_docker_image_url>',
                                   description="The URL of the (ci.tno.nl) docker image file")
    nr_of_models: int = Field(default=1, description="'0' will create a model (container) per ESDL object")


class SimulationPost(BaseModel):
    name: str = 'simulation name'
    start_date: datetime = '2023-01-25 00:00:00'
    time_step_seconds: int = '3600'
    nr_of_time_steps: int = '24'
    max_step_calc_time_minutes: float = Field(default=10,
                                              description="If a time step takes longer than this amount of minutes,"
                                                          " the simulation will be aborted")
    keep_logs_hours: float = '24.0'
    log_level: str = Field(default='info', description="Options: 'debug', 'info', 'warning', 'error'")
    calculation_services: list[CalculationService]
    esdl_base64string: str = '<esdl_file_base64encoded_string>'


class SimulationStatus(SimulationPost):
    simulation_id: str = 'sim-0'
    simulation_status: str = 'Running time step 2 of 24'
    calculation_start_datetime: datetime = datetime.now()
    calculation_end_datetime: typing.Optional[datetime] = None
    calculation_duration: timedelta = timedelta(seconds=3000)

    @classmethod
    def from_simulation_and_status(cls, simulation: Simulation, status: str):
        if simulation.calculation_end_datetime:
            calculation_duration = simulation.calculation_end_datetime - simulation.calculation_start_datetime
        else:
            calculation_duration = datetime.now() - simulation.calculation_start_datetime

        return cls(
            name=simulation.simulation_name,
            start_date=simulation.simulation_start_datetime,
            time_step_seconds=simulation.time_step_seconds,
            nr_of_time_steps=simulation.nr_of_time_steps,
            calculation_services=simulation.calculation_services,
            esdl_base64string=simulation.esdl_base64string,
            log_level=simulation.log_level,
            simulation_id=simulation.simulation_id,
            simulation_status=status,
            calculation_start_datetime=simulation.calculation_start_datetime,
            calculation_end_datetime=simulation.calculation_end_datetime,
            calculation_duration=calculation_duration
        )


class SimulationList(BaseModel):
    simulations: Sequence[SimulationStatus]
