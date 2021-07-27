# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:48:57 2021

@author: Jacob Stonehill
"""

from Experiment import Experiment
from Log import Log
from PyQt5 import QtWidgets
from UI.UI import UI
from Controller import Controller
import sys

if __name__ == "__main__":
    Log.create(name = 'NTP_Log', file_path='app.log', file_format='%(asctime)s : %(process)d : %(levelname)s : %(message)s')
    experiment = Experiment()
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = UI(window)
    Log.attach_ui(ui)
    controller = Controller(ui)
    window.show()
    sys.exit(app.exec_())