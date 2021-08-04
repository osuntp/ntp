# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:48:57 2021

@author: Jacob Stonehill
"""

# from Experiment import Experiment
from SM import SerialMonitor
from Model import Model
from Log import Log
from PyQt5 import QtWidgets
from UI.UI import UI
from Presenter import Presenter
import sys

if __name__ == "__main__":

    # Create Objects
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = UI(window)
    presenter = Presenter()
    model = Model()
    serial_monitor = SerialMonitor()

    # Assign Dependencies
    presenter.ui = ui
    presenter.model = model
    presenter.serial_monitor = serial_monitor
    serial_monitor.model = model

    # Setup
    app.aboutToQuit.connect(serial_monitor.on_window_exit)
    presenter.setup()
    Log.ui = ui
    Log.create(name = 'NTP_Log', file_path='app.log', file_format='%(asctime)s : %(process)d : %(levelname)s : %(message)s')
    serial_monitor.connect_arduinos()


    window.show()
    sys.exit(app.exec_())