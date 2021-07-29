from abc import ABC, abstractmethod

class TestStandState(ABC):

    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def enter_state(self):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def exit_state(self):
        pass