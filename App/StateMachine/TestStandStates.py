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

        self.model.trial_time = 0
        self.model.reset_dataframe()
        self.model.start_button_text = 'Start Trial'
        self.model.state_text = 'STANDBY'
        self.model.trial_is_running = False

        self.presenter.run_attempt_to_activate_start_button()
        self.ui.run.set_pause_button_clickable(False)

        self.test_stand.set_valve_position(90)

    def tick(self):
        pass
    
    def exit_state(self):
        pass

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




# class StandbyState():

#     is_first_start = True
#     ui: UI = None

#     def start(self):
#         Log.info('Test Stand has entered the Standby State')
#         self.model.trial_time = 0
#         self.model.reset_dataframe()
#         self.model.trial_button_text = 'Start Trial'
#         self.model.current_trial_time_stamp_index = 0
#         self.model.trial_is_complete = False
#         self.model.trial_is_running = False
#         self.model.trial_is_paused = False

#         if (self.is_first_start):
#             self.is_first_start = False
#         else:
#             self.ui.run.set_start_button_clickable(True)
#             self.ui.run.set_pause_button_clickable(False)

#     def tick(self):
#         pass

#     def end(self):
#         pass

class IdleState():

    def start(self):
        print('entered idle state and machine is ' + str(self.test_stand))

    def tick(self):
        print('idle state tick')

    def end(self):
        print('exit idle state')

class DemoAutoState():

    trial_end_time = 0
    current_sequence_index: int = 0
    target_mass_flow = 0
    current_valve_position = 0
    delta_valve_position = 0.25
    test_stand: TestStand
    standby_state: StandbyState

    def start(self):
        Log.info('Test Stand has entered the Auto State.')
        self.model.trial_is_running = True
        self.model.trial_is_paused = False
        self.model.last_trial_time_stamp = time.time()
        self.model.trial_button_text = 'Running Trial - ' + str(round(self.model.trial_time, 1))

        #self.test_stand.set_valve_position(self.model.loaded_config.sequence_power[self.current_sequence_index])

        self.target_mass_flow = self.model.loaded_config.sequence_mass_flow_rate[self.current_sequence_index]
        self.target_valve_position = self.model.loaded_config.sequence_valve_position[self.current_sequence_index]
        self.target_power = self.model.loaded_config.sequence_power[self.current_sequence_index]
        self.target_OF_instruction = self.model.loaded_config.sequence_OF_instruction[self.current_sequence_index]

    def tick(self):
        if(self.model.trial_is_running):
            time_stamp = time.time()
            delta_time = time_stamp - self.model.last_trial_time_stamp
            self.model.trial_time = self.model.trial_time + delta_time
            self.model.last_trial_time_stamp = time_stamp

            self.model.trial_button_text = 'Running Trial - ' + str(round(self.model.trial_time, 1))

            # If this is not the last sequence step
            if(self.current_sequence_index <= len(self.model.loaded_config.sequence_time_step)-2):

                # If the trial time has reached the next sequence step
                if(self.model.trial_time >= float(self.model.loaded_config.sequence_time_step[self.current_sequence_index+1])):
                    self.current_sequence_index = self.current_sequence_index+1

                    self.target_mass_flow = self.model.loaded_config.sequence_mass_flow_rate[self.current_sequence_index]
                    self.target_valve_position = self.model.loaded_config.sequence_valve_position[self.current_sequence_index]
                    self.target_power = self.model.loaded_config.sequence_power[self.current_sequence_index]
                    self.target_OF_instruction = self.model.loaded_config.sequence_OF_instruction[self.current_sequence_index]
                    
                    # self.test_stand.set_valve_position(valve_position)
                    # self.model.valve_position = valve_position

            elif(self.model.trial_time >= float(self.model.loaded_config.trial_end_timestep)):
                self.current_sequence_index = 0
                self.model.save_trial_data(is_aborted_trial=False)
                self.trial_end_time = time.time()
                self.model.trial_is_complete = True
                self.model.trial_is_running = False

            
            if self.target_mass_flow: # Control mass flow rate
                # TODO: update mass flow controller algorithm (implement PID?)

                # Determine valve position
                if(self.model.current_mass_flow < (self.target_mass_flow-5)):
                    self.current_valve_position = self.current_valve_position - self.delta_valve_position
                            
                elif(self.model.current_mass_flow > (self.target_mass_flow+5)):
                    self.current_valve_position = self.current_valve_position + self.delta_valve_position
                
                if(self.current_valve_position > 90):
                    self.current_valve_position = 90

                elif(self.current_valve_position < 0):          
                    self.current_valve_position = 0
                
                # Update valve position
                self.test_stand.set_valve_position(self.current_valve_position)
                self.model.valve_position = self.current_valve_position

            elif self.target_valve_position: # Control valve position
                self.current_valve_position = self.target_valve_position
                self.test_stand.set_valve_position(self.current_valve_position)
                self.model.valve_position = self.current_valve_position

            if self.target_power: # Control heater power
                # TODO: implement heater power control system
                # Switching frequency can't be faster than 1/2 AC cycle (e.g., 1/120 s = 8.33 ms)
                # Let's use 10 Hz switching frequency
                # Max power is 520 W, so if you want (say) 260 W, that is a 50 % duty cycle (on for 5 periods, then off for 5 periods)
                # Have to round desired power to nearest 50 ms period (e.g., can't have a 75% duty cycle because that would be on for 7.5 periods, then off for 2.5 periods)
                # In other words, can only have duty cycles as multiples of 10% (520 W, 468, 416, 364, etc.)
                pass


            

            
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
        

    def end(self):
        pass

class DemoIdleState():

    def enter_state(self):
        Log.info('Test Stand has entered the Idle State.')
        self.model.trial_is_running = False
        self.model.trial_is_paused = True

        self.model.trial_button_text = 'Resume Trial at ' + str(round(self.model.trial_time,1))

    def tick(self):
        pass

    def exit_state(self):
        pass