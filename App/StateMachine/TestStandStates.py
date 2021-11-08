from UI.UI import UI
from StateMachine.TestStand import TestStand
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

class DemoStandbyState(AbstractState):

    is_first_start = True
    ui: UI = None

    def enter_state(self):
        Log.info('Test Stand has entered the Standby State')
        self.model.trial_time = 0
        self.model.reset_dataframe()
        self.model.trial_button_text = 'Start Trial'
        self.model.current_trial_time_stamp_index = 0
        self.model.trial_is_complete = False
        self.model.trial_is_running = False
        self.model.trial_is_paused = False

        if (self.is_first_start):
            self.is_first_start = False
        else:
            self.ui.run.set_start_button_clickable(True)
            self.ui.run.set_pause_button_clickable(False)

    def tick(self):
        pass

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
    trial_end_time = 0

    test_stand: TestStand
    standby_state: DemoStandbyState

    def enter_state(self):
        Log.info('Test Stand has entered the Auto State.')
        self.model.trial_is_running = True
        self.model.trial_is_paused = False
        self.model.last_trial_time_stamp = time.time()
        self.model.trial_button_text = 'Running Trial - ' + str(round(self.model.trial_time, 1))

    def tick(self):
        if(self.model.trial_is_running):
            time_stamp = time.time()
            delta_time = time_stamp - self.model.last_trial_time_stamp
            self.model.trial_time = self.model.trial_time + delta_time
            self.model.last_trial_time_stamp = time_stamp

            self.model.trial_button_text = 'Running Trial - ' + str(round(self.model.trial_time, 1))

            if(self.model.trial_time >= float(self.model.loaded_config.trial_end_timestep)):
                self.model.save_trial_data(is_aborted_trial=False)
                self.trial_end_time = time.time()
                self.model.trial_is_complete = True
                self.model.trial_is_running = False

        elif(self.model.trial_is_complete):
            current_time = time.time()

            if(current_time > (self.trial_end_time + 0)):
                self.model.trial_button_text = 'Trial Ended.'

            if(current_time > (self.trial_end_time + 0.5)):
                self.model.trial_button_text = 'Trial Ended. .'

            if(current_time > (self.trial_end_time + 1.0)):
                self.model.trial_button_text = 'Trial Ended. . .'

            if(current_time > (self.trial_end_time + 1.5)):
                self.model.trial_button_text = 'Saving Data.'

            if(current_time > (self.trial_end_time + 2)):
                self.model.trial_button_text = 'Saving Data. .'

            if(current_time > (self.trial_end_time + 2.5)):
                self.model.trial_button_text = 'Saving Data. . .'

            if(current_time > (self.trial_end_time + 3)):
                self.test_stand.switch_state(self.standby_state)
        

    def exit_state(self):
        pass

class DemoIdleState(AbstractState):

    def enter_state(self):
        Log.info('Test Stand has entered the Idle State.')
        self.model.trial_is_running = False
        self.model.trial_is_paused = True

        self.model.trial_button_text = 'Resume Trial at ' + str(round(self.model.trial_time,1))

    def tick(self):
        pass

    def exit_state(self):
        pass