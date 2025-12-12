import enum

SimulatorId = str
SimulationId = str
ModelId = str
EsdlId = str


class ProgressState(enum.IntEnum):
    TERMINATED_FAILED = 0
    TERMINATED_FAILED_POD_DELETED = 1
    REGISTERED = 2
    DEPLOYED = 3
    POD_DELETED = 4
    TERMINATED_SUCCESSFULL = 5
    TERMINATED_SUCCESSFULL_POD_DELETED = 6


ModelState_TERMINATED = (
    ProgressState.TERMINATED_FAILED,
    ProgressState.TERMINATED_SUCCESSFULL,
)

progress_state_description = dict(
    {
        0: "(a) model(s) terminated with an error, the simulation has been terminated",
        1: "(a) model(s) terminated with an error, pods are deleted",
        2: "all models registered",
        3: "all models deployed",
        4: "all podds are deleted",
        5: "all models terminated successfully, the simulation has been terminated",
        6: "all models terminated successfully, the simulation has been terminated and pods are deleted",
    }
)
