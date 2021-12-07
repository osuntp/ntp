from PyQt5.QtCore import endl
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

    trial_end_time = 0
    current_sequence_index: int = 0
    target_mass_flow = 0
    current_valve_position = 0
    delta_valve_position = 0.25
    test_stand: TestStand
    standby_state: DemoStandbyState

    def enter_state(self):
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