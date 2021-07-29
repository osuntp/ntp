from TestStandState import TestStandState

class IdleState(TestStandState):
    def enter_state(self):
        print('entered idle state')

    def tick(self):
        print('idle state tick')

    def exit_state(self):
        print('exit idle state')