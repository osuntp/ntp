import threading
import time
from Log import Log

from SM import SerialMonitor
from SM import Arduino

class TestStand:

    state_machine_stopped = False

    demo_state = None
    current_state = None
    serial_monitor: SerialMonitor = None

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
    
    def set_valve_position(self, new_position):
        Log.info('The Test Stand is setting the valve to the following position: ' + str(new_position))
        message = '<stdin, valve, ' + str(new_position) + '>\n'
        self.serial_monitor.write(Arduino.CONTROLLER, message)