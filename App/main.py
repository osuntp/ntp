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

if __name__ == "__main__":
    Log.create()
    settings = SettingsManager.open_settings_file()

    # Create Objects
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    ui = UI(window, settings)
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
            
            file_location = cwd + '\App\TestStandProfiles\\'
            
            spec = importlib.util.spec_from_file_location('module.name', os.path.join(file_location, file))
            
            module = importlib.util.module_from_spec(spec)
            
            spec.loader.exec_module(module)

            profile = module.TestStandBehaviour()

            profile.test_stand = test_stand

            profiles.append(profile)

            ui.setup.test_stand_behaviour_field.addItem(profile.name)

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

    # Setup
    app.aboutToQuit.connect(serial_monitor.on_window_exit)
    # app.aboutToQuit.connect(model.save_trial_data)
    app.aboutToQuit.connect(test_stand.turn_off_state_machine)
    test_stand.setup(standby_state)
    presenter.setup()
    test_stand.set_profile(settings.profile_index)

    if(settings.developer_mode):
        presenter.setup_developer_mode_clicked()
    else:
        presenter.setup_manual_connect_clicked()

    window.show()
    sys.exit(app.exec_())