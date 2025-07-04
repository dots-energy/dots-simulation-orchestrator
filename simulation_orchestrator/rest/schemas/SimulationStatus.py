from datetime import datetime, timedelta
import typing
from simulation_orchestrator.simulation_logic.simulation_inventory import Simulation
from simulation_orchestrator.rest.schemas.SimulationPost import SimulationPost


class SimulationStatus(SimulationPost):
    simulation_id: str = "sim-0"
    simulation_status: str = "Running time step 2 of 24"
    calculation_start_datetime: datetime = datetime.now()
    calculation_end_datetime: typing.Optional[datetime] = None
    calculation_duration: timedelta = timedelta(seconds=3000)

    @classmethod
    def from_simulation_and_status(cls, simulation: Simulation, status: str):
        if simulation.calculation_end_datetime:
            calculation_duration = (
                simulation.calculation_end_datetime
                - simulation.calculation_start_datetime
            )
        else:
            calculation_duration = (
                datetime.now() - simulation.calculation_start_datetime
            )

        return cls(
            name=simulation.simulation_name,
            start_date=simulation.simulation_start_datetime,
            nr_of_time_steps=simulation.simulation_duration_in_seconds,
            calculation_services=simulation.calculation_services,
            esdl_base64string=simulation.esdl_base64string,
            log_level=simulation.log_level,
            simulation_id=simulation.simulation_id,
            simulation_status=status,
            calculation_start_datetime=simulation.calculation_start_datetime,
            calculation_end_datetime=simulation.calculation_end_datetime,
            calculation_duration=calculation_duration,
        )
