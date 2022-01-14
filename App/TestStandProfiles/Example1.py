if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

import time
import random

class TestStandBehaviour(AbstractProfile):

    name = 'Noahs Mass Flow Control'

    # Sequence Values
    timestep = []
    power = []
    target_mass_flow = []
    OF_instruction = []

    # Other Values
    delta_valve_position = 0.25

    def start(self):
        self.current_step = 0
        self.trial_time = 0

    def tick(self):
        # If this is not the last time step
        if(self.current_step is not len(self.timestep)-1):

            # If the trial time has passed time to move to the next time step
            if(self.trial_time > self.timestep[self.current_step + 1]):
                 self.current_step = self.current_step + 1

        valve_position = self.test_stand.valve.position

        # Open valve if mass flow is too low, Close valve if mass flow is too high

        if(self.test_stand.mass_flow < (self.target_mass_flow[self.current_step]-5)):
            
            # calculate delta_valve_position
            # add it to current valve position
            mass_flow_diff = self.target_mass_flow[self.current_step] - self.test_stand.mass_flow
            if mass_flow_diff > 50:
                self.delta_valve_position = -1
            elif mass_flow_diff > 25:
                self.delta_valve_position = -0.5
            elif mass_flow_diff > 10:
                self.delta_valve_position = -0.5
            else:
                self.delta_valve_position = -0.25

            new_valve_position = valve_position + self.delta_valve_position

            if(new_valve_position < 0):
                new_valve_position = 0
                
            self.test_stand.valve.set_position(new_valve_position)

        elif(self.test_stand.mass_flow > (self.target_mass_flow[self.current_step]+5)):

            mass_flow_diff = self.target_mass_flow[self.current_step] - self.test_stand.mass_flow
            if mass_flow_diff < -50:
                self.delta_valve_position = 1
            elif mass_flow_diff < -25:
                self.delta_valve_position = 0.5
            elif mass_flow_diff < -10:
                self.delta_valve_position = 0.5
            else:
                self.delta_valve_position = 0.25

            new_valve_position = valve_position + self.delta_valve_position

            if(new_valve_position > 90):
                new_valve_position = 90

            self.test_stand.valve.set_position(new_valve_position)
        
    def end(self):
        pass

# EDIT BELOW BUT DO NOT REMOVE
    sidebar_values = [
        'Test 1',
        'Test 2',
        'Test 3',
    ]

    def get_sidebar_values(self):
        return [random.random(), random.random(), random.random()]

    sequence_columns = [
        'Timestep (s)', 
        'Power (W)', 
        'Mass Flow Rate (slm)', 
        'Valve Position', 
        'OF Instruction'
        ]
    
    def set_sequence_values(self, values):
        self.timestep = [float(value) for value in values[0]]
        self.power = [float(value) for value in values[1]]
        self.target_mass_flow = [float(value) for value in values[2]]
        self.OF_instruction = [str(value) for value in values[3]]

    dataframe_columns = [
        'Time', 
        'Mass Flow', 
        'Flow Temperature', 
        'Temperature 1', 
        'Internal Temperature 1', 
        'Temperature 2', 
        'Internal Temperature 2', 
        'Temperature 3', 
        'Internal Temperature 3', 
        'Tank Pressure', 
        'Inlet Pressure', 
        'Valve Position'
        ]

    def get_dataframe_values(self):
        values = [
            time.time(),
            self.test_stand.mass_flow,
            0,
            self.test_stand.inlet_temp,
            0,
            self.test_stand.mid_temp,
            0,
            self.test_stand.outlet_temp,
            0,
            self.test_stand.supply_press,
            self.test_stand.inlet_press,
            self.test_stand.valve.position
        ]

        return values

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehaviour()
    instance.is_valid()