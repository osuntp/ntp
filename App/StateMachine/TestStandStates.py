import Model
import SM
from abc import ABC, abstractmethod

import StateMachine.TestStand
import time
from Log import Log


# All state classes derive from this abstract base class
class AbstractState(ABC):

    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None

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

class DemoAutoState(AbstractState):

    temperature_target: float = 30
    deadzone: float = 10


    last_time_stamp = 0

    def enter_state(self):
        Log.info('Test Stand has entered the Auto State.')
        self.model.trial_is_running = True
        self.model.trial_is_paused = False
        self.last_time_stamp = time.time()

    def tick(self):
        time_stamp = time.time()
        delta_time = time_stamp - self.last_time_stamp
        self.model.trial_time = self.model.trial_time + delta_time
        self.last_time_stamp = time_stamp

    def exit_state(self):
        pass

class DemoIdleState(AbstractState):

    def enter_state(self):
        Log.info('Test Stand has entered the Idle State.')
        self.model.trial_is_running = False
        self.model.trial_is_paused = True

    def tick(self):
        pass

    def exit_state(self):
        pass

class DemoStandbyState(AbstractState):

    def enter_state(self):
        Log.info('Test Stand has entered the Standby State')
        self.model.trial_time = 0
        self.model.trial_is_running = False
        self.model.trial_is_paused = False

    def tick(self):
        pass

    def exit_state(self):
        pass

