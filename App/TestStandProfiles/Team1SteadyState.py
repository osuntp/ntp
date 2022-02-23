if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

import time
from statistics import mean

class TestStandBehavior(AbstractProfile):

    name = 'Team 1 Steady State'

    minimum_time_for_SS_calc = 180 #10 min

    outlet_temps = []
    graphite_temps = []

    outlet_temp_residual = 999
    graphite_temp_residual = 999

    acceptable_outlet_residual = 1
    acceptable_graphite_residual = 2

    def start(self):
        self.test_stand.heater.set_power(self.heater_power[0])
        self.test_stand.valve.set_position(90)

        self.outlet_temps = []
        self.graphite_temps = []

        self.graphite_temp_residual = 999   
        self.outlet_temp_residual = 999

    def tick(self):
        if(not self.checking_for_steady_state[self.current_step]):
            # Move to next step if elapsed time is greater than step duration
            if self.step_time > self.duration[self.current_step]:
                self.move_to_next_step()
                self.test_stand.heater.set_power(self.heater_power[self.current_step])

    def end(self):
        pass
    
    def update_steady_state_values(self):
        self.outlet_temps.append(self.test_stand.sensors.outlet_temp)
        self.graphite_temps.append(self.test_stand.sensors.heater_temp)  

        if(self.step_time > self.minimum_time_for_SS_calc):
            self.outlet_temps.pop(0)
            self.graphite_temps.pop(0)

            #Mean of the first half of outlet_temps array minus the mean of the second half of outlet_temps array
            self.outlet_temp_residual = abs(mean(self.outlet_temps[:len(self.outlet_temps)//2]) - mean(self.outlet_temps[len(self.outlet_temps)//2:]))
            self.graphite_temp_residual = abs(mean(self.graphite_temps[:len(self.graphite_temps)//2]) - mean(self.graphite_temps[len(self.graphite_temps)//2:]))
                  

    def check_if_steady_state_is_reached(self):
        if((self.outlet_temp_residual < self.acceptable_outlet_residual) and (self.graphite_temp_residual < self.acceptable_graphite_residual)):
            self.move_to_next_step()

    # Appear to the left side of the GUI
    sidebar_values = ['In Steady State:', '% SS Eval:', 'Graphite Residual:', 'Outlet Residual:']
    def get_sidebar_values(self):

        percent_value = 100*self.step_time/self.minimum_time_for_SS_calc

        if(percent_value > 100):
            percent_value = 100

        return [
            str(not self.checking_for_steady_state[self.current_step]), 
            str('%.1f' % percent_value),
            str(self.graphite_temp_residual),
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
        if(self.checking_for_steady_state[self.current_step]):
            self.update_steady_state_values()
            self.check_if_steady_state_is_reached()

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