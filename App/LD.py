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
def clean(raw_message_string: str):
    raw_message = raw_message_string.split(sep = ', ')

    clean_message = []
    
    for i in range(len(raw_message)):
        # clean_message_value = re.sub("/[-+]?\d*\.?\d+/", "", raw_message[i])
        clean_message_value = re.sub("\n", "", raw_message[i])
        clean_message.append(clean_message_value)

    if(clean_message[0] == 'da'):
        for i in range(1, len(clean_message)):
            clean_message[i] = float(clean_message[i])
    print(clean_message)
    return clean_message    

def get_new_dataframe():
    return DataFrame(columns=columns)

def append_point_to_frame(data_point, dataframe):
    temp = data_point[0]
    internalTemp = data_point[1]
    dataframe = dataframe.append({'Temperature':temp, 'Internal Temperature':internalTemp}, ignore_index=True)
    
    return dataframe