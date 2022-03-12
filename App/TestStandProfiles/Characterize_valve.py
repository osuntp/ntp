if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

from hashlib import new
import time
import random

class TestStandBehavior(AbstractProfile):

    name = 'Valve Characterization'
        
    def start(self):
        self.start_time = time.time()

    def tick(self):

        # Get current position
        valve_position = self.test_stand.valve.position
        valve_diff = self.valve_delta[self.current_step]
        new_valve_position = valve_position + valve_diff

        # Set new valve position
        self.test_stand.valve.set_position(new_valve_position)

        # Move to next step if elapsed time is greater than step duration
        if (new_valve_position > 90) or (new_valve_position < 0):
            self.move_to_next_step()

    def end(self):
        pass
    
    # Appear to the left side of the GUI
    sidebar_values = []
    def get_sidebar_values(self):
        return []

    # List of controllable variables (e.g., heater, valve position)
    sequence_columns = ['Valve Delta']
    def set_sequence_values(self, values):
        self.valve_delta = [float(value) for value in values[0]]

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
        'Heater Current'
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
            self.test_stand.sensors.heater_current,
        ]

        return values

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    instance.is_valid()