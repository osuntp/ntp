# mplwidget.py

import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class MplWidget(FigureCanvasQTAgg):

    axes: Axes
    xlabel = ''
    ylabel = ''

    def __init__(self, parent = None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super(MplWidget, self).__init__(self.fig)

    def set_labels(self, xlabel: str, ylabel: str):
        self.xlabel = xlabel
        self.ylabel = ylabel

    def update_vals(self, x, y):
        self.axes.cla()       
        self.axes.plot(x,y)
        self.__set_format()        
        self.draw()

    def __set_format(self):
        self.axes.get_figure().subplots_adjust(bottom = 0.2)
        self.axes.set_xticks([-10, -8, -6, -4, -2, 0])
        self.axes.set_yticks([0,5,10,15,20,25,30,35,40,45,50])
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.set_xlim(-10, 0)
        self.axes.set_ylim(0, 50)
        self.axes.margins(0)
        self.axes.grid()