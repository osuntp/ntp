from dataclasses import dataclass
import threading
import time

from pyqtgraph.Qt import App
from SM import Arduino
from UI.UI import UI
from Log import Log


from SM import SerialMonitor
import SM

class BlueLines:

    test_stand = None

    mass_flow_min = 0
    heater_current_min = 0
    heater_temp_min = 0
    inlet_temp_min = 0
    mid_temp_min = 0
    outlet_temp_min = 0
    supply_press_min = 0
    inlet_press_min = 0
    mid_press_min = 0
    outlet_press_min = 0

    mass_flow_max = -1
    heater_current_max = -1
    heater_temp_max = -1
    inlet_temp_max = -1
    mid_temp_max = -1
    outlet_temp_max = -1
    supply_press_max = -1
    inlet_press_max = -1
    mid_press_max = -1
    outlet_press_max = -1

    time_step_sequence = []
    sensor_sequence = []
    limit_type_sequence = []
    value_sequence = []

    next_time_step = 0
    current_sequence_step = 0

    def set_sequence_values(self, time_step, sensor, limit_type, value):
        self.time_step_sequence = time_step
        self.sensor_sequence = sensor
        self.limit_type_sequence = limit_type
        self.value_sequence = value
# ['Mass Flow', 'Heater Current', 'Heater Temp', 'Inlet Temp', 'Midpoint Temp', 'Outlet Temp', 'Supply Press', 'Inlet Press', 'Midpoint Press', 'Outlet Press']

    def condition_is_met(self):
        mass_flow = self.test_stand.mass_flow
        heater_current = self.test_stand.heater_current
        heater_temp = self.test_stand.heater_temp
        in_temp = self.test_stand.inlet_temp
        mid_temp = self.test_stand.mid_temp
        out_temp = self.test_stand.outlet_temp
        supply_press = self.test_stand.supply_press
        in_press = self.test_stand.inlet_press
        mid_press = self.test_stand.mid_press
        out_press = self.test_stand.outlet_press
              
        is_valid = True

        log_output = 'Trial ended early due to blue lines. '

        if(mass_flow < self.mass_flow_min):
            is_valid = False
            log_output = log_output + 'The mass flow was ' + str(mass_flow) + ' which is below the blue line minimum of ' + str(self.mass_flow_min) + '.'
        if(heater_current < self.heater_current_min):
            is_valid = False
            log_output = log_output + 'The heater current was ' + str(heater_current) + ' which is below the blue line minimum of ' + str(self.heater_current_min) + '.'
        if(heater_temp < self.heater_temp_min):
            is_valid = False
            log_output = log_output + 'The heater temperature was ' + str(heater_temp) + ' which is below the blue line minimum of ' + str(self.heater_temp_min) + '.'
        if(in_temp < self.inlet_temp_min):
            is_valid = False
            log_output = log_output + 'The inlet temperature was ' + str(in_temp) + ' which is below the blue line minimum of ' + str(self.inlet_temp_min) + '.'
        if(mid_temp < self.mid_temp_min):
            is_valid = False
            log_output = log_output + 'The midpoint temperature was ' + str(mid_temp) + ' which is below the blue line minimum of ' + str(self.mid_temp_min) + '.'
        if(out_temp < self.outlet_temp_min):
            is_valid = False
            log_output = log_output + 'The outlet temperature was ' + str(out_temp) + ' which is below the blue line minimum of ' + str(self.outlet_temp_min) + '.'
        if(supply_press < self.supply_press_min):
            is_valid = False
            log_output = log_output + 'The supply pressure was ' + str(supply_press) + ' which is below the blue line minimum of ' + str(self.supply_press_min) + '.'
        if(in_press < self.inlet_press_min):
            is_valid = False
            log_output = log_output + 'The inlet pressure was ' + str(in_press) + ' which is below the blue line minimum of ' + str(self.inlet_press_min) + '.'
        if(mid_press < self.mid_press_min):
            is_valid = False
            log_output = log_output + 'The midpoint pressure was ' + str(mid_press) + ' which is below the blue line minimum of ' + str(self.mid_press_min) + '.'
        if(out_press < self.outlet_press_min):
            is_valid = False
            log_output = log_output + 'The outlet pressure was ' + str(out_press) + ' which is below the blue line minimum of ' + str(self.outlet_press_min) + '.'

        if(self.mass_flow_max != -1):
            if(mass_flow > self.mass_flow_max):
                is_valid = False
                log_output = log_output + 'The mass flow was ' + str(mass_flow) + ' which is above the blue line maximum of ' + str(self.mass_flow_max) + '.'
        if(self.heater_current_max != -1):
            if(heater_current > self.heater_current_max):
                is_valid = False
                log_output = log_output + 'The heater_current was ' + str(heater_current) + ' which is above the blue line maximum of ' + str(self.heater_current_max) + '.'
        if(self.heater_temp_max != -1):
            if(heater_temp > self.heater_temp_max):
                is_valid = False
                log_output = log_output + 'The heater temperature was ' + str(heater_temp) + ' which is above the blue line maximum of ' + str(self.heater_temp_max) + '.'
        if(self.inlet_temp_max != -1):
            if(in_temp > self.inlet_temp_max):
                is_valid = False
                log_output = log_output + 'The inlet temperature was ' + str(in_temp) + ' which is above the blue line maximum of ' + str(self.inlet_temp_max) + '. '
        if(self.mid_temp_max != -1):
            if(mid_temp > self.mid_temp_max):
                is_valid = False
                log_output = log_output + 'The midpoint temperature was ' + str(mid_temp) + ' which is above the blue line maximum of ' + str(self.mid_temp_max) + '. '
        if(self.outlet_temp_max != -1):
            if(out_temp > self.outlet_temp_max):
                is_valid = False
                log_output = log_output + 'The outlet temperature was ' + str(out_temp) + ' which is above the blue line maximum of ' + str(self.outlet_temp_max) + '. '
        if(self.supply_press_max != -1):
            if(supply_press > self.supply_press_max):
                is_valid = False
                log_output = log_output + 'The supply pressure was ' + str(supply_press) + ' which is above the blue line maximum of ' + str(self.supply_press_max) + '. '
        if(self.inlet_press_max != -1):
            if(in_press > self.inlet_press_max):
                is_valid = False
                log_output = log_output + 'The inlet pressure was ' + str(in_press) + ' which is above the blue line maximum of ' + str(self.inlet_press_max) + '. '
        if(self.mid_press_max != -1):
            if(mid_press > self.mid_press_max):
                is_valid = False
                log_output = log_output + 'The midpoint pressure was ' + str(mid_press) + ' which is above the blue line maximum of ' + str(self.mid_press_max) + '. '
        if(self.outlet_press_max != -1):
            if(out_press > self.outlet_press_max):
                is_valid = False
                log_output = log_output + 'The outlet pressure was ' + str(out_press) + ' which is above the blue line maximum of ' + str(self.outlet_press_max) + '. '

        if(not is_valid):
            Log.python.info(log_output)

        return is_valid

    def update_sequence(self):
        if(self.current_sequence_step != len(self.time_step_sequence)):

            current_time = time.time()

            while(current_time >= self.time_step_sequence[self.current_sequence_step]):
                sensor = self.sensor_sequence[self.current_sequence_step]
                limit_type = self.limit_type_sequence[self.current_sequence_step]
                value = self.value_sequence[self.current_sequence_step]

                if (limit_type == 'Max'):
                    if(sensor == 'Mass Flow'):
                        self.mass_flow_max = value
                    elif(sensor == 'Heater Current'):
                        self.heater_current_max = value
                    elif(sensor == 'Heater Temp'):
                        self.heater_temp_max = value
                    elif(sensor == 'Inlet Temp'):
                        self.inlet_temp_max = value
                    elif(sensor == 'Midpoint Temp'):
                        self.mid_temp_max = value
                    elif(sensor == 'Outlet Temp'):
                        self.outlet_temp_max = value
                    elif(sensor == 'Supply Press'):
                        self.supply_press_max = value
                    elif(sensor == 'Inlet Press'):
                        self.inlet_press_max = value
                    elif(sensor == 'Midpoint Press'):
                        self.mid_press_max
                    elif(sensor == 'Outlet Press'):
                        self.outlet_press_max = value
                else:
                    if(sensor == 'Mass Flow'):
                        self.mass_flow_min = value
                    elif(sensor == 'Heater Current'):
                        self.heater_current_min = value
                    elif(sensor == 'Heater Temp'):
                        self.heater_temp_min = value
                    elif(sensor == 'Inlet Temp'):
                        self.inlet_temp_min = value
                    elif(sensor == 'Midpoint Temp'):
                        self.mid_temp_min = value
                    elif(sensor == 'Outlet Temp'):
                        self.outlet_temp_min = value
                    elif(sensor == 'Supply Press'):
                        self.supply_press_min = value
                    elif(sensor == 'Inlet Press'):
                        self.inlet_press_min = value
                    elif(sensor == 'Midpoint Press'):
                        self.mid_press_min = value
                    elif(sensor == 'Outlet Press'):
                        self.outlet_press_min = value

                self.current_sequence_step = self.current_sequence_step + 1

                if(self.current_sequence_step == len(self.time_step_sequence)):
                    return

    def start_sequence(self):
        self.mass_flow_min = 0
        self.heater_current_min = 0
        self.heater_temp_min = 0
        self.inlet_temp_min = 0
        self.mid_temp_min = 0
        self.outlet_temp_min = 0
        self.supply_press_min = 0
        self.inlet_press_min = 0
        self.mid_press_min = 0
        self.outlet_press_min = 0

        self.mass_flow_max = -1
        self.heater_current_max = -1
        self.heater_temp_max = -1
        self.inlet_temp_max = -1
        self.mid_temp_max = -1
        self.outlet_temp_max = -1
        self.supply_press_max = -1
        self.inlet_press_max = -1
        self.mid_press_max = -1
        self.outlet_press_max = -1

        self.current_sequence_step = 0

class Heater:

    serial_monitor: SerialMonitor = None

    desired_power: float = 0

    _time_between_updates: float = 3 # seconds between each calculation
    _time_since_last_update: float = 0
    _rms_heater_power: float = 520

    _running_total_weighted_power: float = 0
    _running_total_time: float = 0
    is_on: bool = False
    _previous_timestamp: float = 0

    def __init__(self):
        self._previous_timestamp = time.time()

    def set_power(self, power: float):
        self._running_sum_weighted_power = 0
        self._running_total_time = 0
        self._time_since_last_update = 0

        self.desired_power = power

    def _tick(self):
        if(not self.serial_monitor.is_fully_connected):
            if(self.serial_monitor.tsc_arduino is not None):
                self._turn_off_heater()
            
            return
        self._time_since_last_update = self._time_since_last_update + (time.time() - self._previous_timestamp)
        self._previous_timestamp = time.time()

        if(self._time_since_last_update >= self._time_between_updates):
            self._update_heater()
    
    def _update_heater(self):       
        if(self.is_on):
            self._running_total_weighted_power = self._running_total_weighted_power + (self._rms_heater_power * self._time_since_last_update)

        self._running_total_time = self._running_total_time + self._time_since_last_update

        average_power = self._running_total_weighted_power / self._running_total_time

        print(str(average_power) + " " + str(self.desired_power) + " " + str(self._time_since_last_update))

        if(self.is_on):
            if(average_power > self.desired_power):
                self._turn_off_heater()
        else:
            if(average_power < self.desired_power):
                self._turn_on_heater()

        self._time_since_last_update = 0

    def _turn_off_heater(self):

        message = "<stdin, heater, off>\n"
        self.is_on = False
        self.serial_monitor.write(Arduino.CONTROLLER, message)

    def _turn_on_heater(self):

        message = "<stdin, heater, on>\n"
        self.is_on = True
        self.serial_monitor.write(Arduino.CONTROLLER, message)

class Valve:
    position = 0
    serial_monitor: SerialMonitor = None

    # TODO: ORDERS FROM NOAH: 0 is closed, 90 is open
    def set_position(self, position: float):
        self.position = 90 - position
        message = '<stdin, valve, ' + str(position) + '>\n'

        self.serial_monitor.write(SM.Arduino.CONTROLLER, message)

class Sensors:
    mass_flow = 0
    flow_temp = 0
    heater_current = 0

    heater_temp = 0
    inlet_temp = 0
    mid_temp = 0
    outlet_temp = 0
    
    supply_press = 0
    inlet_press = 0
    mid_press = 0
    outlet_press = 0
    
class TestStand:

    # References
    blue_lines: BlueLines = None
    heater: Heater = None
    valve: Valve = None
    sensors: Sensors = None
    ui: UI = None
    app: App = None
    current_state = None
    serial_monitor: SerialMonitor = None
    trial_running_state = None
    trial_ended_state = None
    profiles = []

    # Trial Values
    trial_time = 0
    end_trial_time = 0

    # Other
    state_machine_stopped = False

    def setup(self, initial_state):
        self.heater = Heater()
        self.heater.serial_monitor = self.serial_monitor
        self.ui.manual.heater_field.setMaximum(self.heater._rms_heater_power)

        self.valve = Valve()
        self.valve.serial_monitor = self.serial_monitor

        self.sensors = Sensors()

        self.blue_lines = BlueLines()
        self.blue_lines.test_stand = self

        self.current_state = initial_state
        self.current_state.enter_state()

        self.tick_thread = threading.Thread(target = self.tick)
        self.tick_thread.start()

    def tick(self):
        while(True):
            if(self.state_machine_stopped):
                return

            self.heater._tick()

            self.current_state.tick()
            time.sleep(0.1)

    def switch_state(self, new_state):
        self.current_state.exit_state()

        self.current_state = new_state

        self.current_state.enter_state()

    def turn_off_state_machine(self):
        self.state_machine_stopped = True
    
    def set_profile(self, i):
        profile = self.profiles[i]

        self.trial_running_state.set_current_profile(profile)
        self.ui.configuration.set_sequence_table_columns(profile.sequence_columns)
        self.ui.run.set_sequence_table_columns(profile.sequence_columns)

    def end_trial(self):
        self.switch_state(self.trial_ended_state)