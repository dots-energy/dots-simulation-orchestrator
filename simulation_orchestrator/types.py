import enum
from uuid import UUID

SO_ID = str
SimulationId = str
ModelId = UUID


class ProgressState(enum.IntEnum):
    TERMINATED_FAILED = 0
    REGISTERED = 1
    DEPLOYED = 2
    PARAMETRIZED = 3
    STEP_STARTED = 4
    STEP_FINISHED = 5
    TERMINATED_SUCCESSFULL = 6


ModelState_TERMINATED = (ProgressState.TERMINATED_FAILED, ProgressState.TERMINATED_SUCCESSFULL)

progress_state_description = dict({
    '0': '(a) model(s) terminated with an error, the simulation has been terminated',
    '1': 'all models registered',
    '2': 'all models deployed',
    '3': 'all models parametrized',
    '4': 'started with calculation step',
    '5': 'finished calculation step',
    '6': 'the simulation terminated successfully'
})
