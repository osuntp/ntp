import threading
import time
from UI.UI import UI
from Log import Log


from SM import SerialMonitor
from SM import Arduino

class TestStand:

    state_machine_stopped = False
    ui: UI = None
    current_state = None
    serial_monitor: SerialMonitor = None
    trial_running_state = None
    profiles = []

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
        self.current_state.enter_state()

        self.current_state = new_state

        self.current_state.exit_state()

    def turn_off_state_machine(self):
        self.state_machine_stopped = True
    
    def set_profile(self, i):
        profile = self.profiles[i]

        self.trial_running_state.set_current_profile(profile)
        self.ui.configuration.set_sequence_table_columns(profile.columns)

    def set_valve_position(self, new_position):
        Log.info('Test Stand sending message to TSC to set valve to following position: ' + str(new_position))
        message = '<stdin, valve, ' + str(new_position) + '>\n'
        self.serial_monitor.write(Arduino.CONTROLLER, message)