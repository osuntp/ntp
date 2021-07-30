from abc import ABC, abstractmethod

import TestStand

# All state classes derive from this abstract base class
class AbstractState(ABC):

    def __init__(self, test_stand: TestStand):
        self.test_stand = test_stand

    @abstractmethod
    def enter_state(self):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def exit_state(self):
        pass

class IdleState(AbstractState):

    def enter_state(self):
        print('entered idle state and machine is ' + str(self.test_stand))

    def tick(self):
        print('idle state tick')

    def exit_state(self):
        print('exit idle state')

