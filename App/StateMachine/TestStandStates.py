from UI.UI import UI
from StateMachine.TestStand import TestStand
import Model
import SM

import time
from Log import Log

class StandbyState():

    model: Model.Model = None
    presenter = None
    serial_monitor: SM.SerialMonitor = None
    ui: UI = None
    test_stand: TestStand = None

    def enter_state(self):
        Log.info('Test Stand has entered the Standby State')
        
        self.model.start_button_text = 'Start Trial'
        self.model.state_text = 'STANDBY'
        self.model.trial_is_running = False

        self.presenter.run_attempt_to_activate_start_button()
        self.ui.run.set_pause_button_clickable(False)
        
        if(self.serial_monitor.is_fully_connected):
            self.test_stand.set_valve_position(90)

    def tick(self):
        pass
    
    def exit_state(self):
        pass

class ConnectingState():

    test_stand: TestStand = None
    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None
    standby_state: StandbyState = None

    ui: UI = None

    start_time = 0

    daq_port: str = None
    tsc_port: str = None


    def enter_state(self):
        self.start_time = time.time()
        self.ui.setup.manual_connect_button.setEnabled(False)
        self.ui.setup.developer_mode_field.setEnabled(False)
        self.model.connect_arduinos_button_enabled = False

    def tick(self):
        time_passed = time.time() - self.start_time

        if(time_passed > 0):
            text = 'Connecting.'

        if(time_passed > 0.5):
            text = 'Connecting. .'

        if(time_passed > 1):
            text = 'Connecting. . .'

        if(time_passed > 1.5):
            self.serial_monitor.connect_arduinos(self.daq_port, self.tsc_port)
            self.test_stand.switch_state(self.standby_state)
        else:
            self.model.daq_status_text = text
            self.model.tsc_status_text = text

    def exit_state(self):
        self.ui.setup.manual_connect_button.setEnabled(True)
        self.ui.setup.developer_mode_field.setEnabled(True)
        self.model.connect_arduinos_button_enabled = True
        
class TrialEndedState():

    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None
    test_stand: TestStand = None
    ui: UI = None
    standby_state: StandbyState = None

    start_timestamp = 0
    text = ''

    def enter_state(self):
        self.model.trial_is_running = False
        self.model.run_sequence_bolded_row = -1
        self.model.save_trial_data(False)
        self.model.reset_dataframe()
        self.model.state_text = 'ENDING'

        Log.info('Trial Ended.')
        self.ui.run.set_pause_button_clickable(False)
        self.start_timestamp = time.time()

    def tick(self):
        timestamp = time.time()
        time_passed = timestamp - self.start_timestamp

        if(time_passed > 0):
            text = 'Trial Ended.'

        if(time_passed > 0.5):
            text = 'Trial Ended. .'

        if(time_passed > 1):
            text = 'Trial Ended. . .'

        if(time_passed > 1.5):
            text = 'Saving Data.'

        if(time_passed > 2):
            text = 'Saving Data. .'

        if(time_passed > 2.5):
            text = 'Saving Data. . .'

        self.model.start_button_text = text

        if(time_passed > 3):
            self.test_stand.switch_state(self.standby_state)

    def exit_state(self):
        pass

class TrialRunningState():
    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None
    test_stand: TestStand = None
    ui: UI = None
    trial_ended_state: TrialEndedState = None

    start_timestamp = 0

    current_profile = None

    def enter_state(self):
        self.model.reset_dataframe()
        self.start_timestamp = time.time()
        self.trial_time = 0
        self.current_sequence_row = 0
        self.model.trial_is_running = True
        self.model.state_text = 'RUNNING'
        self.ui.run.set_start_button_runningtrial()
        self.ui.run.set_pause_button_clickable(True)

        self.current_profile.start()

    def tick(self):
        self.test_stand.trial_time = time.time() - self.start_timestamp
        self.current_profile.trial_time = self.test_stand.trial_time

        if(self.test_stand.trial_time > self.test_stand.end_trial_time):
            self.test_stand.end_trial()
            return

        time_string = '%.1f' % self.test_stand.trial_time

        self.model.start_button_text = 'Running Trial - ' + time_string
        self.model.run_sequence_bolded_row = self.current_profile.current_step

        self.current_profile.tick()

    def exit_state(self):
        self.model.trial_is_running = False
        self.current_profile.end()

    def set_current_profile(self, profile):
        self.current_profile = profile