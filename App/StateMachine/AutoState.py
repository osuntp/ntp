from TestStandState import TestStandState

class AutoState(TestStandState):
    def enter_state(self):
        print('entered auto state')

    def tick(self):
        print('auto state tick')

    def exit_state(self):
        print('exit auto state')