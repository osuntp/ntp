if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

import time
class TestStandBehavior(AbstractProfile):

    name = 'Test Facility Characterization'

    def start(self):
        self.test_stand.heater.set_power(self.heater_power[0])
        self.start_time = time.time()

    def tick(self):
        
        # Get current valve position
        valve_position = self.test_stand.valve.position

        # Open valve if mass flow is too low, Close valve if mass flow is too high
        if(self.test_stand.sensors.mass_flow < (self.mass_flow[self.current_step]-5)):
            
            # calculate delta_valve_position
            # add it to current valve position
            mass_flow_diff = self.mass_flow[self.current_step] - self.test_stand.sensors.mass_flow
            if mass_flow_diff > 50:
                self.delta_valve_position = 1
            elif mass_flow_diff > 25:
                self.delta_valve_position = 0.5
            elif mass_flow_diff > 10:
                self.delta_valve_position = 0.5
            else:
                self.delta_valve_position = 0.25

            new_valve_position = valve_position + self.delta_valve_position

            if(new_valve_position > 90):
                new_valve_position = 90
                
            self.test_stand.valve.set_position(new_valve_position)

        elif(self.test_stand.sensors.mass_flow > (self.mass_flow[self.current_step]+5)):

            mass_flow_diff = self.mass_flow[self.current_step] - self.test_stand.sensors.mass_flow
            if mass_flow_diff < -50:
                self.delta_valve_position = -1
            elif mass_flow_diff < -25:
                self.delta_valve_position = -0.5
            elif mass_flow_diff < -10:
                self.delta_valve_position = -0.5
            else:
                self.delta_valve_position = -0.25

            new_valve_position = valve_position + self.delta_valve_position

            if(new_valve_position < 0):
                new_valve_position = 0

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
    sequence_columns = ['Duration','Heater Power','Mass Flow']
    def set_sequence_values(self,values):
        self.duration = [float(value) for value in values[0]]
        self.heater_power = [float(value) for value in values[1]]
        self.mass_flow = [float(value) for value in values[2]]

    # List of variables appearing in saved data CSV
    dataframe_columns = [
        'Time',
        'Elapsed Time',
        'Mass Flow',
        'Target Mass Flow',
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
        'Heater Current'
        ]
        
    def get_dataframe_values(self):

        values = [
            time.time(),
            self.trial_time,
            self.test_stand.sensors.mass_flow,
            self.mass_flow[self.current_step],
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
            self.test_stand.sensors.heater_current
        ]

        return values

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    
    instance.is_valid()