# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:48:57 2021

@author: Jacob Stonehill
"""
import time
from Data import Data
from Arduino import Arduino
import threading

class Experiment:

    def __init__(self):
        # Variables
        self.experiment_is_running = False
        
        # Dependencies
        self.arduino = Arduino()

        
    def run(self):
        if(self.experiment_is_running):
            print('Warning: Experiment: run(): You tried to run an experiment while one was already running.')
            return
        
        self.dataframe = Data.get_new_dataframe()

        self.arduino.open_serial()
        
        time.sleep(0.5)
        
        # Run data collection loop on separate thread. Otherwise it will impede GUI event loop.
        self.data_collection_thread = threading.Thread(target = self.experiment_loop)
        self.data_collection_thread.start()  
        
    def experiment_loop(self):
        print('Data collection has started.')
        self.experiment_is_running = True
        
        while(self.experiment_is_running):
            
            if(self.arduino.data_point_is_available()):
                raw_data_point = self.arduino.get_data_point()             
                clean_data_point = Data.clean(raw_data_point)  
                
                self.dataframe = Data.append_point_to_frame(clean_data_point, self.dataframe)         
    
    def stop(self):
        self.experiment_is_running = False
        self.data_collection_thread.join()
        self.arduino.close_serial()
        
        Data.save_to_csv(self.dataframe)
        
        print('Data collection has stopped. CSV file is available.')