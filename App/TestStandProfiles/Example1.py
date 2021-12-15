class TestStandBehaviour:

    name = 'Example 1 Profile'
    columns = ['Timestep (s)', 'Mass Flow (slm)']

    current_step = 0
    trial_time = 0
    timestep = []
    mass_flow = []

    def start(self):
        self.current_step = 0

    def tick(self):
        pass

    def end(self):
        pass

    def set_sequence_values(self, values):
        self.timestep = values[0]
        self.mass_flow = values[1]
