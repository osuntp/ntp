import pandas
import LD
from Log import Log
from typing import List
import time

class Model:

    hidden_data_buffer = 15000 # time in milliseconds (must be in ms since arduino is reporting ms)
    shown_data_buffer = 10000 # time in milliseconds (must be in ms since arduino is reporting ms)

    latest_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.trial_data: pandas.DataFrame = LD.get_new_dataframe()
        self.temp_data: pandas.DataFrame = LD.get_new_dataframe()

    def update(self, message: List):
        self.trial_data = LD.append_point_to_frame(message, self.trial_data)
        self.temp_data = LD.append_point_to_frame(message, self.temp_data)

        LD.drop_old_data_from_frame(self.hidden_data_buffer, self.temp_data)

        self.latest_values = message

        print('model: update: The temperature is ' + str(self.latest_values[4]))
        print('model: update: The time is ' + str(self.latest_values[0]))

    def get_ui_data(self, name: str):

        data_column = [0]

        if not(self.temp_data.empty):

            data_column = self.temp_data[name].tolist()
            time_column = self.temp_data['Time'].tolist()

            latest_time_stamp = time_column[-1]
            time_cutoff = latest_time_stamp - self.shown_data_buffer  

            while(time_column[0] < time_cutoff):
                time_column.pop(0)
                data_column.pop(0)
                
        return data_column

