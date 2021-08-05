# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 04:53:51 2021

@author: Jacob Stonehill
"""
from pandas import DataFrame
import datetime
import re
from typing import List

columns = ['Time', 'Temperature', 'Pressure']

# TODO: Settle on how we want CSV file names to be generated
def __new_save_file_name():
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return 'ExperimentData_' + current_time + '.csv'

def save_to_csv(dataframe: DataFrame):
    CSV_file_name = __new_save_file_name()
    dataframe.to_csv(CSV_file_name)

# TODO: Revisit, we'll want a different reg ex so that we can handle other types of messages from arduino (like ID and errors)
def clean(raw_message_string: str):

    split = raw_message_string.split('<')
    clean_message_string = split[1].split('>')[0]
    clean_message = clean_message_string.split(sep = ', ')

    if(clean_message[0] == 'da'):
        for i in range(1, len(clean_message)):
            clean_message[i] = float(clean_message[i])
    return clean_message    

def get_new_dataframe():
    return DataFrame(columns=columns)

def append_point_to_frame(data_point: List, dataframe: DataFrame):

    time = data_point[0]
    temperature = data_point[1]
    pressure = data_point[2]

    dataframe = dataframe.append({'Time':time, 'Temperature':temperature, 'Pressure':pressure}, ignore_index=True)
    
    return dataframe

def drop_old_data_from_frame(buffer: float, dataframe: DataFrame):
    time_column = dataframe['Time']
    latest_time_stamp = time_column.iloc[-1]
    time_cutoff = latest_time_stamp - buffer

    while(dataframe['Time'].iloc[0] < time_cutoff):
        dataframe.drop(index = dataframe.index[0], inplace = True)