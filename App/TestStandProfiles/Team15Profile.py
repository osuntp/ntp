if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###
import time
class TestStandBehavior(AbstractProfile):

    def start(self):
        self.test_stand.heater.set_power(self.heater_power[0])

    def tick(self):
        # get T exit
        t_exit = self.test_stand.sensors.outlet_temp
        # get valve position
        valve = self.test_stand.valve.position
        # calculate dT
        error = t_exit - self.desired_t_exit[self.current_step]
        # use method to get new valve position
        newPos = self.Celsius2degree(valve,error)
        # send command for new valve position
        self.test_stand.valve.set_position(newPos)
        # check for next sequence step
        if self.step_time > self.duration[self.current_step]:
            self.move_to_next_step()
            self.test_stand.heater.set_power(self.heater_power[self.current_step])

    def end(self):
        pass
    
    def Celsius2degree(self, valve,error):
        Kp = .8
        Ki = .25
        Kd = .1
        dt = .1 # set time step
        # begin PID math
        I = 0
        P = Kp * error
        I = I + (error * Ki * dt)
        D = (Kd / dt) * (error - error)

        u = P + I + D
        delPos = valve * .15;        # 15 percent change in current deflection
        for value in u:
            
            if value > 0:
                newPos = valve - delPos
            elif value < 0:
                newPos = valve + delPos
            else:
                newPos = valve
        return newPos

    sidebar_values = ["T_dif"]
    def get_sidebar_values(self):
        return [self.test_stand.sensors.outlet_temp - self.desired_t_exit[self.current_step]]

    sequence_columns = ["Duration (s)","Heater Power (W)","Desired T_exit (C)"]
    def set_sequence_values(self,values):
        self.duration = [float(value) for value in values[0]]
        self.heater_power = [float(value) for value in values[1]]
        self.desired_t_exit = [float(value) for value in values[2]]

    dataframe_columns = [        'Time',
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
            'Desired T_exit']
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
            self.desired_t_exit
        ]
        return values
### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehavior()
    instance.is_valid()
