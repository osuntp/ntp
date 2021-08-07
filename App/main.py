# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:48:57 2021

@author: Jacob Stonehill
"""

# from Experiment import Experiment
from StateMachine.TestStandStates import DemoState
from StateMachine.TestStand import TestStand
from SM import SerialMonitor
from Model import Model
from Log import Log
from PyQt5 import QtWidgets
from UI.UI import UI
from UI.UI import Window
from Presenter import Presenter
import sys

if __name__ == "__main__":

    # Create Objects
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    ui = UI(window)
    presenter = Presenter()
    model = Model()
    serial_monitor = SerialMonitor()
    # test_stand = TestStand()
    # demo_state = DemoState()

    # Assign Dependencies
    presenter.ui = ui
    presenter.model = model
    presenter.serial_monitor = serial_monitor
    serial_monitor.model = model
    # test_stand.demo_state = demo_state
    # demo_state.serial_monitor = serial_monitor
    # demo_state.model = model
    Log.ui = ui

    # Setup
    Log.create(name = 'NTP_Log', file_path='app.log', file_format='%(asctime)s : %(process)d : %(levelname)s : %(message)s')
    # app.aboutToQuit.connect(serial_monitor.on_window_exit)
    # app.aboutToQuit.connect(test_stand.turn_off_state_machine)
    # serial_monitor.connect_arduinos()
    # test_stand.setup()
    presenter.setup()

    window.show()
    sys.exit(app.exec_())