if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

from hashlib import new
import time
import random

from numpy import sign

class TestStandBehavior(AbstractProfile):

    name = 'Mass Flow Controller Evaluation'
        
    def start(self):
        self.test_stand.heater.set_power(self.heater_power[0])
        self.start_time = time.time()

    def tick(self):

        # Get current position
        valve_position = self.test_stand.valve.position

        # Calculate graded delta valve position based on magnitude of mass_flow_diff
        mass_flow_diff = self.target_mass_flow[self.current_step] - \
            self.test_stand.sensors.mass_flow
        if abs(mass_flow_diff) > 50:
            self.delta_valve_position = 0.5
        elif abs(mass_flow_diff) > 25:
            self.delta_valve_position = 0.25
        elif abs(mass_flow_diff) > 5:
            self.delta_valve_position = 0.2
        elif abs(mass_flow_diff) > 2.5:
            self.delta_valve_position = 0.1
        else:
            # If mass_flow_diff is less than 2.5, don't change valve
            self.delta_valve_position = 0

        # Close or open the valve depending on whether mass_flow_diff is positive or negative
        new_valve_position = valve_position + sign(mass_flow_diff) * \
            self.delta_valve_position

        # Set new valve position
        if self.controller_state[self.current_step] > 0.5:
            self.test_stand.valve.set_position(new_valve_position)

        # Move to next step if elapsed time is greater than step duration
        if self.step_time > self.duration[self.current_step]:
            self.move_to_next_step()
            self.test_stand.heater.set_power(self.heater_power[self.current_step])

    def end(self):
        pass
    
    # Appear to the left side of the GUI
    sidebar_values = []
    def get_sidebar_values(self):
        return []

    # List of controllable variables (e.g., heater, valve position)
    sequence_columns = ['Duration','Heater Power','Target Mass Flow','Controller State']
    def set_sequence_values(self, values):
        self.duration = [float(value) for value in values[0]]
        self.heater_power = [float(value) for value in values[1]]
        self.target_mass_flow = [float(value) for value in values[2]]
        self.controller_state = [float(value) for value in values[3]]

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
        'Target Mass Flow',
        'Controller State'
        ]
        
    def get_dataframe_values(self):

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
            self.target_mass_flow[self.current_step],
            self.controller_state[self.current_step]
        ]

        return values

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    instance.is_valid()