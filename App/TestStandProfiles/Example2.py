if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

class TestStandBehavior(AbstractProfile):

    def start(self):
        pass

    def tick(self):
        pass

    def end(self):
        pass

    sidebar_values = ['OpenFOAM Progress', 'Duration Remaining', 'Datapoints Collected']

    openfoam_progress = 0
    duration_remaining = 0
    num_of_datapoints = 0


    def get_sidebar_values(self):
        return [self.openfoam_progress, self.duration_remaining, self.num_of_datapoints]

    sequence_columns = []
    def set_sequence_values(self):
        pass

    dataframe_columns = []
    def get_dataframe_values(self):
        return []

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    instance.is_valid()