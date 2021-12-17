from StateMachine.TestStand import TestStand


class TestStandBehaviour:

    name = 'Noahs Mass Flow Control'
    columns = ['Timestep (s)', 'Power (W)', 'Mass Flow Rate (slm)', 'Valve Position', 'OF Instruction']

    # Sequence Values
    timestep = []
    power = []
    target_mass_flow = []
    OF_instruction = []

    # Other Values
    delta_valve_position = 0

    # DO NOT REMOVE
    current_step = 0
    trial_time = 0
    test_stand: TestStand = None
    
    def start(self):
        self.current_step = 0
        self.trial_time = 0

    def tick(self):
        # If this is not the last time step
        if(self.current_step is not len(self.timestep)-1):

            # If the trial time has passed time to move to the next time step
            if(self.trial_time > self.timestep[self.current_step + 1]):
                 self.current_step = self.current_step + 1

        valve_position = self.test_stand.valve_position

        # Open valve if mass flow is too low, Close valve if mass flow is too high
        if(self.test_stand.mass_flow < (self.target_mass_flow[self.current_step]-5)):
            valve_position = valve_position - self.delta_valve_position
        elif(self.test_stand.mass_flow > (self.target_mass_flow[self.current_step]+5)):
            valve_position = valve_position + self.delta_valve_position

        # Set limits of valve
        if(valve_position > 90):
            valve_position = 90
        elif(valve_position < 0):
            valve_position = 0

        self.test_stand.set_valve_position(valve_position)

    def end(self):
        pass

    # EDIT BUT DO NOT REMOVE
    def set_sequence_values(self, values):
        self.timestep = [float(value) for value in values[0]]
        self.power = [float(value) for value in values[1]]
        self.target_mass_flow = [float(value) for value in values[2]]
        self.OF_instruction = [str(value) for value in values[3]]
