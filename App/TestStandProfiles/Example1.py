class TestStandBehaviour:

    name = 'Example 1 Profile'
    columns = ['Timestep (s)', 'Mass Flow (slm)']


    timestep = []
    mass_flow = []

    def start(self):
        pass

    def tick(self):
        pass

    def end(self):
        pass

    def set_test_sequence_variables(self, values):
        self.timestep = values[0]
        self.mass_flow = values[1]
