import threading
import time
import TestStandStates

class TestStand:

    state_machine_stopped = False

    def __init__(self):
        self.idle_state = TestStandStates.IdleState(self)

        self.current_state = self.idle_state
        self.current_state.enter_state()

        self.tick_thread = threading.Thread(target = self.tick)
        self.tick_thread.start()

    def tick(self):
        while(True):
            if(self.state_machine_stopped):
                return
            self.current_state.tick()
            time.sleep(0.5)

    def switch_state(self, new_state):
        self.current_state.exit_state()

        self.current_state = new_state

        self.current_state.enter_state()

    def turn_off_state_machine(self):
        self.state_machine_stopped = True

if __name__ == "__main__":
    instance = TestStand()

    instance.turn_off_state_machine()
    instance.tick_thread.join()