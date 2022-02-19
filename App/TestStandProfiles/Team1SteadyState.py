if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

import time
from statistics import mean

class TestStandBehavior(AbstractProfile):

    name = 'Team 1 Steady State'

    # We want this value to be 1500 for tests
    num_of_values_for_ss = 1500

    old_outlet_temps = []
    current_outlet_temps = []

    outlet_temp_residual = 999
    acceptable_residual = 0.5


    def start(self):
        self.test_stand.heater.set_power(self.heater_power[0])
        self.start_time = time.time()

        self.old_outlet_temps = []
        self.current_outlet_temps = []
        self.outlet_temp_residual = 999

    def tick(self):
        if(self.checking_for_steady_state[self.current_step]):

            if(self.steady_state_condition_is_met()):
                self.move_to_next_step()
            
        else:
            # Move to next step if elapsed time is greater than step duration
            if self.step_time > self.duration[self.current_step]:
                self.move_to_next_step()
                self.test_stand.heater.set_power(self.heater_power[self.current_step])

    def end(self):
        pass
    
    def update_steady_state_values(self):
        self.current_outlet_temps.append(self.test_stand.sensors.outlet_temp)

        if(len(self.current_outlet_temps) > self.num_of_values_for_ss):
            value = self.current_outlet_temps.pop(0)
            self.old_outlet_temps.append(value)

            if(len(self.old_outlet_temps) > self.num_of_values_for_ss):
                self.old_outlet_temps.pop(0)

                self.outlet_temp_residual = abs(mean(self.old_outlet_temps) - mean(self.current_outlet_temps))
            
    def steady_state_condition_is_met(self):
        if(len(self.old_outlet_temps) == self.num_of_values_for_ss):
            return (self.outlet_temp_residual < self.acceptable_residual)
        else:
            return False
            
    # Appear to the left side of the GUI
    sidebar_values = ['In Steady State:', '% SS Eval:', 'Outlet Residual:']
    def get_sidebar_values(self):
        return [
            str(not self.checking_for_steady_state[self.current_step]), 
            '%.1f' % float(100*(len(self.old_outlet_temps)+len(self.current_outlet_temps))/(2*self.num_of_values_for_ss)), 
            str(self.outlet_temp_residual)
            ]

    # List of controllable variables (e.g., heater, valve position)
    sequence_columns = ['Duration', 'Heater Power', 'Check For Steady State']
    def set_sequence_values(self, values):
        self.duration = [float(value) for value in values[0]]
        self.heater_power = [float(value) for value in values[1]]
        self.checking_for_steady_state = [float(value) > 0.5 for value in values[2]]

    # List of variables appearing in saved data CSV
    dataframe_columns = [
        'Time',
        'Elapsed Time',
        'Mass Flow',
        'MFM Temperature', 
        'Inlet Temperature',
        'Midpoint Temperature',
        'Outlet Temperature',
        'Heater Temperature',
        'Supply Pressure', 
        'Inlet Pressure',
        'Midpoint Pressure',
        'Outlet Pressure', 
        'Valve Position',
        'Heater Power',
        'Heater Current',
        'Checking For Steady State'
        ]
        
    def get_dataframe_values(self):
        
        self.update_steady_state_values()

        values = [
            time.time(),
            self.trial_time,
            self.test_stand.sensors.mass_flow,
            self.test_stand.sensors.flow_temp,
            self.test_stand.sensors.inlet_temp,
            self.test_stand.sensors.mid_temp,
            self.test_stand.sensors.outlet_temp,
            self.test_stand.sensors.heater_temp,
            self.test_stand.sensors.supply_press,
            self.test_stand.sensors.inlet_press,
            self.test_stand.sensors.mid_press,
            self.test_stand.sensors.outlet_press,
            self.test_stand.valve.position,
            self.test_stand.heater.desired_power,
            self.test_stand.sensors.heater_current,
            str(self.checking_for_steady_state[self.current_step])
        ]

        return values

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    
    instance.is_valid()