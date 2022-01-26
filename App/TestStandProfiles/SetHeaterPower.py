if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

import time

class TestStandBehavior(AbstractProfile):

    name = "Set Heater Power"

    timestamp = []
    desired_heater_power = []

    def start(self):
        pass

    def tick(self):
        # If this is not the last time step
        if(self.current_step is not len(self.timestep)-1):

            # If the trial time has passed time to move to the next time step
            if(self.trial_time > self.timestep[self.current_step + 1]):
                self.current_step = self.current_step + 1

                self.test_stand.heater.set_power(self.desired_heater_power[self.current_step])
                
    def end(self):
        pass

    sidebar_values = ['Desired Power']
    def get_sidebar_values(self):
        return [self.desired_heater_power[self.current_step]]

    sequence_columns = ['Timestamp', 'Heater Power']
    def set_sequence_values(self, values):
        self.timestamp = values[0]
        self.desired_heater_power = values[1]

    dataframe_columns = ['Time (s)', 'Desired Power', 'Heater Current', 'Inlet Temperature', 'Mid Temperature', 'Outlet Temperature']
    def get_dataframe_values(self):
        return [time.time(), self.desired_heater_power[self.current_step], self.test_stand.sensors.heater_current, self.test_stand.sensors.inlet_temp, self.test_stand.mid_temp, self.test_stand.sensors.outlet_temp]

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    instance.is_valid()