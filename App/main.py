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

if __name__ == "__main__":

    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    log_file_name = 'app_' + str(current_time) + '.log'
    Log.create(log_name = 'NTP_Log', file_name=log_file_name, file_format='%(asctime)s : %(process)d : %(levelname)s : %(message)s')

    # Create Objects
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    ui = UI(window)
    presenter = Presenter()
    model = Model()
    serial_monitor = SerialMonitor()
    test_stand = TestStand()
    standby_state = TestStandStates.DemoStandbyState()
    idle_state = TestStandStates.DemoIdleState()
    auto_state = TestStandStates.DemoAutoState()

    # Assign Dependencies
    Log.ui = ui
    standby_state.model = model
    standby_state.serial_monitor = serial_monitor

    idle_state.model = model
    idle_state.serial_monitor = serial_monitor

    auto_state.model = model
    auto_state.serial_monitor = serial_monitor    

    presenter.ui = ui
    presenter.model = model
    presenter.test_stand = test_stand
    presenter.serial_monitor = serial_monitor
    presenter.test_stand_standby_state = standby_state
    presenter.test_stand_idle_state = idle_state
    presenter.test_stand_auto_state = auto_state
    presenter.app = app
    serial_monitor.model = model

    # Setup
    app.aboutToQuit.connect(serial_monitor.on_window_exit)
    # app.aboutToQuit.connect(model.save_trial_data)
    app.aboutToQuit.connect(test_stand.turn_off_state_machine)
    test_stand.setup(standby_state)
    presenter.setup()

    window.show()
    sys.exit(app.exec_())