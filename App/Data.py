# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 04:53:51 2021

@author: Jacob Stonehill
"""
from pandas import DataFrame
import datetime
import re

class Data:     
    
    columns = ['Temperature', 'Internal Temperature']
    
    @staticmethod
    def __new_save_file_name():
        now = datetime.datetime.now()
        current_time = now.strftime("%H%M%S")
        return 'ExperimentData_' + current_time + '.csv'
    
    @classmethod
    def get_new_dataframe(cls):
        return DataFrame(columns=cls.columns)
        
    @staticmethod
    # Parameters: List of strings
    # Uses regular expressions to reduce each element to a string of numbers and periods. Then casts each element to a float
    # Return: List of floats
    def clean(data_point):
        
        clean_data_point = []
        
        for i in range(len(data_point)):
            numbers_as_string = re.sub("/[-+]?\d*\.?\d+/", "", data_point[i])
            
            numbers_as_float = float(numbers_as_string)
            
            clean_data_point.append(numbers_as_float)
            
        return clean_data_point              
    
    @staticmethod
    def append_point_to_frame(data_point, dataframe):
        temp = data_point[0]
        internalTemp = data_point[1]
        dataframe = dataframe.append({'Temperature':temp, 'Internal Temperature':internalTemp}, ignore_index=True)
        
        return dataframe

    @staticmethod
    def save_to_csv(dataframe):
        CSV_file_name = Data.__new_save_file_name()
        dataframe.to_csv(CSV_file_name)