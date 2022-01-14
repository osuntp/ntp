if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

class TestStandBehaviour(AbstractProfile):

    def start(self):
        pass

    def tick(self):
        pass

    def end(self):
        pass

    sidebar_values = []
    def get_sidebar_values(self):
        return []

    sequence_columns = []
    def set_sequence_values(self):
        pass

    dataframe_columns = []
    def get_dataframe_values(self):
        return []

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehaviour()
    instance.is_valid()