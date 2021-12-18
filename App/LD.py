# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 04:53:51 2021

@author: Jacob Stonehill
"""
from pandas import DataFrame
import datetime
import os
from typing import List

# columns = ['Time', 'Mass Flow', 'Heater Current', 'Heater TC', 'Heater TC IT', 'Inlet TC', 'Inlet TC IT', 'Midpoint TC', 'Midpoint TC IT', 'Outlet TC', 'Outlet TC IT', 'Tank Pressure', 'Inlet Pressure', 'Midpoint Pressure', 'Outlet Pressure', 'Valve Position', 'Heater Status', 'OpenFOAM Progress']
columns = ['Time', 'Mass Flow', 'Flow Temperature', 'Temperature 1', 'Internal Temperature 1', 'Temperature 2', 'Internal Temperature 2', 'Temperature 3', 'Internal Temperature 3', 'Tank Pressure', 'Inlet Pressure', 'Valve Position']

# TODO: Settle on how we want CSV file names to be generated
def __new_save_file_name(trial_name: str, is_aborted_trial: bool):
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    
    if(is_aborted_trial):
        prefix = 'ABORTED_'
    else:
        prefix = ''

    return current_time + '_' + prefix + 'trial_data_' + trial_name + '_'  + '.csv'

def save_to_csv(dataframe: DataFrame, trial_name: str, is_aborted_trial: bool):

    folder_name = 'Saved_Data/'

    isdir = os.path.isdir(folder_name)

    if not (isdir):
        os.mkdir(folder_name)

    CSV_file_name = __new_save_file_name(trial_name, is_aborted_trial)

    dataframe.to_csv(folder_name + CSV_file_name)

# TODO: Revisit, we'll want a different reg ex so that we can handle other types of messages from arduino (like ID and errors)
def clean(raw_message_string: str):

    split = raw_message_string.split('<')
    clean_message_string = split[1].split('>')[0]
    clean_message = clean_message_string.split(sep = ', ')

    if(clean_message[0] == 'stdout'):
        for i in range(1, len(clean_message)):
            clean_message[i] = float(clean_message[i])
            
    return clean_message    

def get_new_dataframe():
    return DataFrame(columns=columns)

def append_point_to_frame(message: list, dataframe: DataFrame):

    # time = data_point[0]
    # inlet_temp = data_point[1]
    # midpoint_temp = data_point[2]
    # exit_temp = data_point[3]
    # heat_sink_temp = data_point[4]
    # inlet_pressure = data_point[5]
    # midpoint_pressure = data_point[6]
    # exit_pressure = data_point[7]
    
    # pressure = data_point[2]
    data_point = {}
    for i in range(len(columns)):
        data_point[columns[i]] = message[i]

    dataframe = dataframe.append(data_point, ignore_index=True)
    return dataframe

def drop_old_data_from_frame(buffer: float, dataframe: DataFrame):
    time_column = dataframe['Time']
    latest_time_stamp = time_column.iloc[-1]
    time_cutoff = latest_time_stamp - buffer

    while(dataframe['Time'].iloc[0] < time_cutoff):
        dataframe.drop(index = dataframe.index[0], inplace = True)