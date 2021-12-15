from Config import Config
import pandas
import LD
from Log import Log
from typing import List
import time

class Model:

    daq_status_text = 'Not Connected'
    controller_status_text = 'Not Connected'
    trial_button_text = 'Start'

    hidden_data_buffer = 90 # time in seconds

    latest_values = [0]

    time_between_plot_points = 0.1
    time_of_last_plot_point = 0

    last_trial_time_stamp = 0
    trial_time = 0
    trial_is_running = False

    daq_is_connected = False
    controller_is_connected = False

    valve_position = 90 # 90 degrees = closed
    heater_status = 0
    openFOAM_progress = 0
    mass_flow_rate = 0
    OF_instruction = 0 # TODO: change to str?

    config_is_loaded = False
    bolded_config_row = 0

    current_trial_time_stamp_index = 0

    plot1_buffer = 10
    plot2_buffer = 10
    plot3_buffer = 10
    plot4_buffer = 10

    current_mass_flow:float = 0

    def __init__(self):
        self.reset_dataframe()
        self.ui_run_data: pandas.DataFrame = LD.get_new_dataframe()
        self.ui_diagnostics_data: pandas.DataFrame = LD.get_new_dataframe()

    def update(self, message: List):
        current_time = time.time()
        message.insert(0, current_time)
        message.append(self.valve_position)

        self.current_mass_flow = message[1]

        # message.append(self.heater_status)
        # message.append(self.openFOAM_progress)

        # Add data point to diagnostics dataframe
        self.ui_diagnostics_data = LD.append_point_to_frame(message, self.ui_diagnostics_data)
        
        while((self.latest_values[0] - self.ui_diagnostics_data['Time'].iloc[0]) > self.hidden_data_buffer):
            
            self.ui_diagnostics_data = self.ui_diagnostics_data.iloc[1: , :]

        if(self.trial_is_running):

            # Add data point to trial data frame if trial is running
            self.trial_data = LD.append_point_to_frame(message, self.trial_data)

            if((current_time - self.time_of_last_plot_point) >= self.time_between_plot_points):
                self.time_of_last_plot_point = current_time

                # Add data point to run dataframe
                self.ui_run_data = LD.append_point_to_frame(message, self.ui_run_data)

                while((self.latest_values[0] - self.ui_run_data['Time'].iloc[0]) > self.hidden_data_buffer):
                    self.ui_run_data = self.ui_run_data.iloc[1: , :]                  

        self.latest_values = message        

    def get_run_plot_data(self, name: str):
        if(self.ui_run_data.empty):
            return [0], [0]

        data_column = self.ui_run_data[name].tolist()
        time_column = self.ui_run_data['Time'].tolist()

        len_data = len(data_column)
        len_time = len(time_column)

        if(len_data != len_time):
            if len(data_column) < len(len_time):
               len_time = len_time[: len(data_column)]
            elif len(data_column) > len(len_time):
                data_column = data_column[: len(len_time)]

        latest_time_stamp = self.latest_values[0]

        # time_cutoff = latest_time_stamp - shown_data_buffer 

        # while(time_column[0] <= time_cutoff):
            
        #     time_column.pop(0)
        #     data_column.pop(0)

        #     if(len(time_column) == 0):
        #         return [0], [0]

        for i in range(len(data_column)):
            time_column[i] = float(round((time_column[i] - latest_time_stamp), 2))
            data_column[i] = float(data_column[i])

        return time_column, data_column

    def get_diagnostics_plot_data(self, name: str):

        if(self.ui_diagnostics_data.empty):
            return [], []

        data_column = self.ui_diagnostics_data[name].tolist()
        time_column = self.ui_diagnostics_data['Time'].tolist()

        len_data = len(data_column)
        len_time = len(time_column)

        if(len_data != len_time):
            if len(data_column) < len(len_time):
               len_time = len_time[: len(data_column)]
            elif len(data_column) > len(len_time):
                data_column = data_column[: len(len_time)]

        latest_time_stamp = self.latest_values[0]

        time_cutoff = latest_time_stamp - self.shown_data_buffer  

        while(time_column[0] < time_cutoff):
            time_column.pop(0)
            data_column.pop(0)

        for i in range(len(data_column)):
            time_column[i] = float(round((time_column[i] - latest_time_stamp), 2))
            data_column[i] = float(data_column[i])
            
            # print(time_column[i])

        if(len(time_column == 0)):
            time_column = [0]
            data_column = [0]

        return time_column, data_column

    def save_trial_data(self, is_aborted_trial: bool):
        LD.save_to_csv(self.trial_data, self.loaded_config.trial_name, is_aborted_trial)

    def reset_dataframe(self):
        self.trial_data = LD.get_new_dataframe()