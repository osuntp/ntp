import threading
import time

from pyqtgraph.Qt import App
from UI.UI import UI
from Log import Log


from SM import SerialMonitor
import SM

class TestStand:

    # References
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

    # Test Stand Values
    valve_position = 90

    inlet_temp = 0
    mid_temp = 0
    outlet_temp = 0

    inlet_press = 0
    mid_press = 0
    outlet_press = 0
    tank_press = 0

    mass_flow = 0
    heater_temp = 0

    # Other
    state_machine_stopped = False

    def setup(self, initial_state):
        self.current_state = initial_state
        self.current_state.enter_state()

        self.tick_thread = threading.Thread(target = self.tick)
        self.tick_thread.start()

    def tick(self):
        while(True):
            if(self.state_machine_stopped):
                return

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

    def set_valve_position(self, new_position):
        Log.info('Test Stand sending message to TSC to set valve to following position: ' + str(new_position))

        self.valve_position = new_position
        message = '<stdin, valve, ' + str(new_position) + '>\n'

        self.serial_monitor.write(SM.Arduino.CONTROLLER, message)