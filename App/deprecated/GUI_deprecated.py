# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:19:04 2021

@author: Jacob Stonehill
"""

from tkinter import Tk
from tkinter import Button
from tkinter import StringVar
from tkinter import Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# This class was not refactored since it will be replaced with QT designer
class GUI:
    
    def __init__(self, experiment): 
        self.experiment = experiment
        
        self.plots_are_animating = False
        
    def start(self):
        self.window = Tk()

        self.window.title('Plotting in Tkinter')
        self.window.geometry("1600x900")
        
        self.run_button = Button(master = self.window, command = self.run, height = 2, width = 15, text = "Run Experiment")
        # test_button = Button(master = self.window, command = self.stop, height = 2, width = 15, text = "Stop Experiment")
        
        self.run_button.grid(row=0,column=0)
        # test_button.grid(row=1,column=0)
        
        self.fig = Figure(figsize = (14,8), dpi = 100)   
        
        self.statustext = StringVar()
        
        self.statustext.set('Status: Ready')
        
        self.statusLabel = Label(master = self.window, textvariable = self.statustext, font = ("Aerial", 20)).grid(row=0,column=1)

        self.plot1 = self.fig.add_subplot(121)
        self.plot2 = self.fig.add_subplot(122)
        
        self.plot1.set_xlim(0,50)        
        self.plot1.set_ylim(20,35)
        self.plot2.set_xlim(0,50)
        self.plot2.set_ylim(20,35)
        
        self.plot1.set_title('Temperature - Current Value: ----')
        self.plot2.set_title('Internal Temperature - Current Value: ----')
        

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.window)   
        
        self.canvas.get_tk_widget().grid(row=3, column=1, columnspan=2) 

        self.ani = FuncAnimation(self.fig, self.animate, init_func = self.animate_init, interval=1000)

        self.window.mainloop()
        
    def run(self):
        self.run_button.config(text = 'Stop Experiment', command = self.stop)
        self.statustext.set('Status: Recording...')

        self.experiment.run()
    
    def animate_init(self):
        pass
    
    def set_plots_are_animating(self, isAnimating):
        self.plots_are_animating = isAnimating
    
    def animate(self, i):
        if(self.plots_are_animating):
        
            dataframe = self.experiment.dataframe

            if not(dataframe.empty):
                self.plot1.cla()
                self.plot1.plot(dataframe.index, dataframe['Temperature'])
                
                self.plot2.cla()
                self.plot2.plot(dataframe.index, dataframe['Internal Temperature'])
                
                self.plot1.set_title('Temperature - Current Value: ' + str(dataframe.iat[-1,0]))
                self.plot2.set_title('Internal Temperature - Current Value: ' + str(dataframe.iat[-1,1]))
                
                self.plot1.set_ylim(20,35)
                self.plot1.set_xlim(0,50)
                self.plot2.set_ylim(20,35)
                self.plot2.set_xlim(0,50)
                
                self.canvas.draw()
    
    def stop(self):
        self.statustext.set('Status: Ready')
        self.run_button.config(text = 'Run Experiment', command = self.run)
        
        self.ani.event_source.stop()
        self.experiment.stop()