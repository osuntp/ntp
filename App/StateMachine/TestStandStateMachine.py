import threading
import time
from IdleState import IdleState
from AutoState import AutoState
class TestStandStateMachine:

    state_machine_stopped = False

    def __init__(self):
        self.idle_state = IdleState(self)
        self.auto_state = AutoState(self)

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
    instance = TestStandStateMachine()

    time.sleep(5)
    instance.switch_state(instance.auto_state)
    time.sleep(5)
    instance.switch_state(instance.idle_state)
    time.sleep(3)
    instance.turn_off_state_machine()
    instance.tick_thread.join()