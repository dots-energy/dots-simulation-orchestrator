#  This work is based on original code developed and copyrighted by TNO 2023.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO

import enum

SimulatorId = str
SimulationId = str
ModelId = str


class ProgressState(enum.IntEnum):
    TERMINATED_FAILED = 0
    REGISTERED = 1
    DEPLOYED = 2
    PARAMETERIZED = 3
    STEP_STARTED = 4
    STEP_FINISHED = 5
    TERMINATED_SUCCESSFULL = 6


ModelState_TERMINATED = (ProgressState.TERMINATED_FAILED, ProgressState.TERMINATED_SUCCESSFULL)

progress_state_description = dict({
    0: '(a) model(s) terminated with an error, the simulation has been terminated',
    1: 'all models registered',
    2: 'all models deployed',
    3: 'all models parameterized',
    4: 'started with calculation step',
    5: 'finished calculation step',
    6: 'the simulation terminated successfully'
})
