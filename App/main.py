import types
from StateMachine import TestStandStates
from StateMachine.TestStand import TestStand
from SM import SerialMonitor
from Model import Model
from Log import Log
from PyQt5 import QtWidgets
from UI.UI import UI
from UI.UI import Window
from Presenter import Presenter
import sys
import os
import importlib.util
from SettingsManager import SettingsManager

def profile_is_valid(profile):
    if(not getattr(profile, "start", None)):
        Log.python.error()
        return False
    else:
        if(not callable(getattr(profile, "start", None))):
            print("there is something called start but it is not a method")
            return False
        elif(profile.start() is not None):
            print("there is a start method, but it returns the wrong type")
            



    return True                

if __name__ == "__main__":
    Log.create()
    settings = SettingsManager.open_settings_file()

    # Create Objects
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    ui = UI(window)
    presenter = Presenter()
    model = Model()
    serial_monitor = SerialMonitor()
    test_stand = TestStand()

    standby_state = TestStandStates.StandbyState()
    trial_ended_state = TestStandStates.TrialEndedState()
    trial_aborted_state = TestStandStates.TrialAbortedState()
    trial_running_state = TestStandStates.TrialRunningState()
    connecting_state = TestStandStates.ConnectingState()

    cwd = os.getcwd()

    profiles = []

    for file in os.listdir('App/TestStandProfiles'):

        if file.endswith('.py'):
            if(file != "AbstractProfile.py"):
                file_location = cwd + '\App\TestStandProfiles\\'
                spec = importlib.util.spec_from_file_location('PythonFile', os.path.join(file_location, file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                try:
                    profile = module.TestStandBehaviour()

                    should_load = profile_is_valid(profile)

                    if(should_load):
                        profile.test_stand = test_stand
                        profiles.append(profile)

                        try:
                            ui.setup.test_stand_behaviour_field.addItem(profile.name)
                        except AttributeError:
                            ui.setup.test_stand_behaviour_field.addItem(file)
                except ModuleNotFoundError:
                    Log.python.error("Tried to create proile from /TestStandProfiles/" + file + ", but there was no \"TestStandBehaviour\" class found.")

                
    test_stand.profiles = profiles

    ui.setup.set_initial_values_from_settings(settings.profile_index, settings.developer_mode)

    # Assign Dependencies
    ui.app = app

    model.test_stand = test_stand
    model.test_stand_standby_state = standby_state
    model.test_stand_trial_running_state = trial_running_state
    model.serial_monitor = serial_monitor
    model.ui = ui

    test_stand.ui = ui
    test_stand.serial_monitor = serial_monitor
    test_stand.trial_running_state = trial_running_state
    test_stand.trial_ended_state = trial_ended_state

    standby_state.model = model
    standby_state.serial_monitor = serial_monitor
    standby_state.ui = ui
    standby_state.presenter = presenter
    standby_state.test_stand = test_stand
    trial_running_state.test_stand = test_stand
    trial_running_state.model = model
    trial_running_state.ui = ui
    trial_aborted_state.model = model
    trial_aborted_state.test_stand = test_stand
    trial_aborted_state.standby_state = standby_state
    trial_ended_state.standby_state = standby_state
    trial_ended_state.ui = ui
    trial_ended_state.test_stand = test_stand
    trial_ended_state.model = model
    connecting_state.model = model
    connecting_state.serial_monitor = serial_monitor
    connecting_state.standby_state = standby_state
    connecting_state.test_stand = test_stand
    connecting_state.ui = ui

    presenter.ui = ui
    presenter.model = model
    presenter.test_stand = test_stand
    presenter.serial_monitor = serial_monitor
    presenter.test_stand_standby_state = standby_state
    presenter.test_stand_trial_running_state = trial_running_state
    presenter.test_stand_trial_aborted_state = trial_aborted_state
    aborted_state = trial_aborted_state
    presenter.test_stand_trial_ended_state = trial_ended_state
    presenter.test_stand_connecting_state = connecting_state
    presenter.app = app

    serial_monitor.model = model
    serial_monitor.test_stand = test_stand
    serial_monitor.test_stand_connecting_state = connecting_state

    # Setup
    app.aboutToQuit.connect(serial_monitor.on_window_exit)
    # app.aboutToQuit.connect(model.save_trial_data)
    app.aboutToQuit.connect(test_stand.turn_off_state_machine)
    test_stand.setup(connecting_state)
    presenter.setup(settings.profile_index)

    if(settings.developer_mode):
        presenter.setup_developer_mode_clicked()

    window.show()
    sys.exit(app.exec_())