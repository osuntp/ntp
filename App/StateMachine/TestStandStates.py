import Model
import SM
from abc import ABC, abstractmethod

import StateMachine.TestStand

# All state classes derive from this abstract base class
class AbstractState(ABC):

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

class DemoState(AbstractState):

    temperature_target: float = 30
    deadzone: float = 10
    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None

    heater_is_on = False

    def enter_state(self):
        pass

    def tick(self):
        temperature = self.model.temperature

        print(temperature)

        if temperature is None:
            return

        # Is it too cold, then turn on the heater
        if(not self.model.heater_is_on and temperature < (self.temperature_target - self.deadzone)):
            self.serial_monitor.write(SM.Arduino.DAQ, "<heater, on>")

            self.heater_is_on = True

        # Is it too hot, then turn off the heater
        elif(self.model.heater_is_on and temperature > (self.temperature_target + self.deadzone)):
            self.serial_monitor.write(SM.Arduino.DAQ, "<heater, off>")

            self.heater_is_on = False

    def exit_state(self):
        pass



