import threading
import time

class TestStand:

    state_machine_stopped = False

    demo_state = None
    current_state = None

    def setup(self):
        self.current_state = self.demo_state
        self.current_state.enter_state()

        self.tick_thread = threading.Thread(target = self.tick)
        self.tick_thread.start()

    def tick(self):
        while(True):
            if(self.state_machine_stopped):
                return

            self.current_state.tick()
            time.sleep(0.001)

    def switch_state(self, new_state):
        self.current_state.exit_state()

        self.current_state = new_state

        self.current_state.enter_state()

    def turn_off_state_machine(self):
        self.state_machine_stopped = True