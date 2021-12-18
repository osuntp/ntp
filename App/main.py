# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:48:57 2021

@author: Jacob Stonehill
"""

# from Experiment import Experiment

from StateMachine import TestStandStates
from StateMachine.TestStand import TestStand
from SM import SerialMonitor
from Model import Model
import datetime
from Log import Log
from PyQt5 import QtWidgets
from UI.UI import UI
from UI.UI import Window
from Presenter import Presenter
import sys
import os
import importlib.util

def create_log():
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    log_file_name = 'app_' + str(current_time) + '.log'
    Log.create(log_name = 'NTP_Log', file_name=log_file_name, file_format='%(asctime)s : %(process)d : %(levelname)s : %(message)s')

if __name__ == "__main__":

    create_log()

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
    trial_running_state = TestStandStates.TrialRunningState()

    cwd = os.getcwd()

    profiles = []

    for file in os.listdir("App/TestStandProfiles"):
        if file.endswith(".py"):
            
            file_location = cwd + '\App\TestStandProfiles\\'
            
            spec = importlib.util.spec_from_file_location("module.name", os.path.join(file_location, file))
            
            module = importlib.util.module_from_spec(spec)
            
            spec.loader.exec_module(module)

            profile = module.TestStandBehaviour()

            profile.test_stand = test_stand

            profiles.append(profile)

            ui.setup.test_stand_behaviour_field.addItem(profile.name)

    test_stand.profiles = profiles

    # Assign Dependencies
    Log.ui = ui

    ui.app = app

    model.test_stand = test_stand

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
    trial_ended_state.standby_state = standby_state
    trial_ended_state.ui = ui
    trial_ended_state.test_stand = test_stand
    trial_ended_state.model = model

    # auto_state.model = model
    # auto_state.test_stand = test_stand
    # auto_state.standby_state = standby_state
    # auto_state.serial_monitor = serial_monitor    

    presenter.ui = ui
    presenter.model = model
    presenter.test_stand = test_stand
    presenter.serial_monitor = serial_monitor
    presenter.test_stand_standby_state = standby_state
    presenter.test_stand_trial_running_state = trial_running_state
    presenter.test_stand_trial_ended_state = trial_ended_state
    presenter.app = app

    serial_monitor.model = model
    serial_monitor.presenter = presenter

    # Setup
    app.aboutToQuit.connect(serial_monitor.on_window_exit)
    # app.aboutToQuit.connect(model.save_trial_data)
    app.aboutToQuit.connect(test_stand.turn_off_state_machine)
    test_stand.setup(standby_state)
    presenter.setup()
    test_stand.set_profile(0)

    window.show()
    sys.exit(app.exec_())