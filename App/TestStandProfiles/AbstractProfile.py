from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from StateMachine.TestStand import TestStand

class AbstractProfile(ABC):
    test_stand: TestStand = None
    current_step = 0
    trial_time = 0

    def is_valid(self):
        _is_valid = True

        self.sequence_step

