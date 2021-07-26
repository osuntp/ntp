# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:48:57 2021

@author: Jacob Stonehill
"""

from Experiment import Experiment
from PyQt5 import QtWidgets
from UI.UI import UI
from Controller import Controller
import sys

if __name__ == "__main__":

    experiment = Experiment()
    app = QtWidgets.QApplication(sys.argv)
    
    window = QtWidgets.QMainWindow()

    # UI must be instanciated before Controller, it is a parameter for the constructor
    ui = UI(window)
    controller = Controller(ui)

    window.show()
    sys.exit(app.exec_())