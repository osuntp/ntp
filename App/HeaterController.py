# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:49:45 2021

@author: stone
"""
import time

class HeaterController:
    def __init__(self):
        pass
    
    voltage = 0;
    currentTemp = 0;
    minTemp = 100;
    maxTemp = 105;
    
    emergencyShutDownTemp = 115;
    
    experimentIsRunning = False;
    
    def StartControlLoop(self):
        pass
    
    def GetCurrentTemperature(self):
        return 5
    
    def AdjustVoltage(self, newvoltage):
        voltage = newvoltage
        print(voltage)
    
    def SetExperimentStatus(self, isActive):
        self.experimentIsRunning = isActive;
        
        if self.experimentIsRunning:
            self.StartControlLoop()
    

        

        