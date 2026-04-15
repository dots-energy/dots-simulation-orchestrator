from dataclasses import dataclass


@dataclass
class FmuSimulationStatus:
    has_error: bool
    error_message: str
    simulation_id: str
