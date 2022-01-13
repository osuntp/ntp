from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from StateMachine.TestStand import TestStand

class AbstractProfile():
    test_stand: 'TestStand' = None
    current_step = 0
    
    sequence_step_count = 0
    trial_time = 0

    def move_to_next_sequence_step(self):
        self.current_step = self.current_step + 1

        if(self.current_step > self.sequence_step_count - 1):
            self.test_stand.end_trial()

    def end_trial(self):
        self.test_stand.end_trial()