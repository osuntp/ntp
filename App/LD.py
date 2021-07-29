# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 04:53:51 2021

@author: Jacob Stonehill
"""
from pandas import DataFrame
import datetime
import re

columns = ['Temperature', 'Internal Temperature']

# TODO: Settle on how we want CSV file names to be generated
def __new_save_file_name():
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return 'ExperimentData_' + current_time + '.csv'

def save_to_csv(dataframe: DataFrame):
    CSV_file_name = __new_save_file_name()
    dataframe.to_csv(CSV_file_name)

# TODO: Revisit, we'll want a different reg ex so that we can handle other types of messages from arduino (like ID and errors)
def clean(data_point: str):
    clean_data_point = []
    
    for i in range(len(data_point)):
        numbers_as_string = re.sub("/[-+]?\d*\.?\d+/", "", data_point[i])
        
        numbers_as_float = float(numbers_as_string)
        
        clean_data_point.append(numbers_as_float)
        
    return clean_data_point    

def get_new_dataframe():
    return DataFrame(columns=columns)

def append_point_to_frame(data_point, dataframe):
    temp = data_point[0]
    internalTemp = data_point[1]
    dataframe = dataframe.append({'Temperature':temp, 'Internal Temperature':internalTemp}, ignore_index=True)
    
    return dataframe