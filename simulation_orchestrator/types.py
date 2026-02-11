import enum

SimulatorId = str
SimulationId = str
ModelId = str
EsdlId = str


class ProgressState(enum.IntEnum):
    TERMINATED_FAILED = 0
    TERMINATED_FAILED_POD_DELETED = 1
    TERMINATED_DEPLOYMENT_FAILED = 2
    REGISTERED = 3
    DEPLOYED = 4
    POD_DELETED = 5
    TERMINATED_SUCCESSFULL = 6
    TERMINATED_SUCCESSFULL_POD_DELETED = 7


ModelState_TERMINATED = (
    ProgressState.TERMINATED_FAILED,
    ProgressState.TERMINATED_SUCCESSFULL,
)

progress_state_description = dict(
    {
        0: "(a) model(s) terminated with an error, the simulation has been terminated",
        1: "(a) model(s) terminated with an error, pods are deleted",
        2: "(a) deployment(s) failed, the simulation has been terminated",
        3: "all models registered",
        4: "all models deployed",
        5: "all podds are deleted",
        6: "all models terminated successfully, the simulation has been terminated",
        7: "all models terminated successfully, the simulation has been terminated and pods are deleted",
    }
)
