from Config import Config
import pandas
import LD
from Log import Log
from typing import List
import time

class Model:

    hidden_data_buffer = 90 # time in seconds
    shown_data_buffer = 10
    diagnostics_data_buffer = 15

    latest_values = [0]

    time_between_plot_points = 0.5
    time_of_last_run_plot_point = 0
    time_of_last_diagnostics_plot_point = 0

    trial_is_running = False

    config_is_loaded = False
    loaded_config_trial_name = ''

    plot1_buffer = 10
    plot2_buffer = 10
    plot3_buffer = 10
    plot4_buffer = 10
    
    test_stand = None
    test_stand_trial_running_state = None
    test_stand_standby_state = None
    serial_monitor = None
    ui = None

# Values for UI Display

    # Side Bar
    state_text = 'STANDBY'
    abort_button_enabled = False

    # Setup Page
    daq_status_text = 'Not Connected'
    tsc_status_text = 'Not Connected'
    connect_arduinos_button_enabled = True
    developer_checkbox_enabled = True

    # Diagnostics Page


    # Run Page
    start_button_text = 'Start Trial'
    run_sequence_bolded_row = -1
    start_button_enabled = False
    stop_button_enabled = False
    load_button_enabled = True

    def __init__(self):
        self.ui_run_data: pandas.DataFrame = LD.get_new_dataframe(LD.columns)
        self.ui_diagnostics_data: pandas.DataFrame = LD.get_new_dataframe(LD.columns)

    def update(self, message: List):
        current_time = time.time()
        message.insert(0, current_time)
        message.append(self.test_stand.valve.position)
        message.append(self.test_stand.heater.is_on)
        
        # print(message)

        # 0 - Time 
        # 1 - Mass Flow
        # 2 - Flow Temperature
        # 3 - Heater Current
        # 4 - Heater Temperature
        # 5 - (IT) Heater Temperature
        # 6 - Inlet Temperature
        # 7 - (IT) Inlet Temperature
        # 8 - Midpoint Temperature
        # 9 - (IT) Midpoint Temperature
        # 10 - Outlet Temperature
        # 11 - (IT) Outlet Temperature
        # 12 - Supply Pressure
        # 13 - Inlet Pressure
        # 14 - Midpoint Pressure
        # 15 - Outlet Pressure
        # 16 - Valve Position
        # 17 - Heater Status

        self.test_stand.mass_flow = message[1]
        self.test_stand.flow_temp = message[2]
        self.test_stand.heater_current = message[3]
        self.test_stand.heater_temp = message[4]
        self.test_stand.inlet_temp = message[6]
        self.test_stand.mid_temp = message[8]
        self.test_stand.outlet_temp = message[10]
        self.test_stand.supply_press = message[12]
        self.test_stand.inlet_press = message[13]
        self.test_stand.mid_press = message[14]
        self.test_stand.outlet_press = message[15]

        # Add data point to diagnostics dataframe      
        if((current_time - self.time_of_last_diagnostics_plot_point) >= self.time_between_plot_points):
                self.time_of_last_diagnostics_plot_point = current_time

                # Add data point to run dataframe
                self.ui_diagnostics_data = LD.append_point_to_frame(self.ui_diagnostics_data, message, LD.columns)

                while((message[0] - self.ui_diagnostics_data['Time'].iloc[0]) > self.diagnostics_data_buffer):           
                    self.ui_diagnostics_data = self.ui_diagnostics_data.iloc[1: , :]

        if(self.trial_is_running):
            # Add data point to trial data frame if trial is running
            self.trial_data = LD.append_point_to_frame(self.trial_data, self.test_stand.trial_running_state.current_profile.get_dataframe_values(), self.test_stand.trial_running_state.current_profile.dataframe_columns)

            if((current_time - self.time_of_last_run_plot_point) >= self.time_between_plot_points):
                self.time_of_last_run_plot_point = current_time

                # Add data point to run dataframe
                self.ui_run_data = LD.append_point_to_frame(self.ui_run_data, message, LD.columns)

                while((current_time - self.ui_run_data['Time'].iloc[0]) > self.hidden_data_buffer):
                    self.ui_run_data = self.ui_run_data.iloc[1: , :]

    def get_run_plot_data(self, name: str, buffer: float):
        if(self.ui_run_data.empty):
            return [0], [0]

        data_column = self.ui_run_data[name].tolist()
        time_column = self.ui_run_data['Time'].tolist()

        latest_time_stamp = time.time()

        time_cutoff = latest_time_stamp - buffer

        while(time_column[0] <= time_cutoff):           
            time_column.pop(0)
            data_column.pop(0)

            if(len(time_column) == 0):
                return [0], [0]

        for i in range(len(data_column)):
            time_column[i] = float((time_column[i] - latest_time_stamp))
            data_column[i] = float(data_column[i])

        return time_column, data_column

    def get_diagnostics_plot_data(self, name: str):

        if(self.ui_diagnostics_data.empty):
            return [0], [0]

        data_column = self.ui_diagnostics_data[name].tolist()
        time_column = self.ui_diagnostics_data['Time'].tolist()

        latest_time_stamp = time.time()

        for i in range(len(data_column)):
            time_column[i] = float(round((time_column[i] - latest_time_stamp), 2))
            data_column[i] = float(data_column[i])

        return time_column, data_column

    def save_trial_data(self, is_aborted_trial: bool):
        LD.save_to_csv(self.trial_data, self.loaded_config_trial_name, is_aborted_trial)

    def reset_dataframe(self):
        self.trial_data = LD.get_new_dataframe(self.test_stand.trial_running_state.current_profile.dataframe_columns)

    def set_config(self, config: Config):
        current_profile_name = self.test_stand_trial_running_state.current_profile.name

        config_is_valid = (config.profile_name == current_profile_name)

        if(config_is_valid):
            Log.python.info('Trial configuration has been loaded to run page.')

            self.config_is_loaded = True
            self.loaded_config_trial_name = config.trial_name

            self.test_stand.end_trial_time = float(config.trial_end_timestep)
            self.test_stand_trial_running_state.current_profile.set_sequence_values(config.sequence_values)
            self.test_stand_trial_running_state.current_profile.step_count = len(config.sequence_values[0])

            self.test_stand.blue_lines.set_sequence_values(config.blue_lines_time_step, config.blue_lines_sensor_type, config.blue_lines_limit_type, config.blue_lines_value)
            self.ui.run.set_sequence_table(config.sequence_values, self.test_stand.end_trial_time)
            
        else:
            Log.python.info('Tried to load configuration to run page, but the configuration was invalid.')
            self.config_is_loaded = False
            self.loaded_config_trial_name = 'Invalid CONFIG File'
   
        self.try_to_enable_start_button()

    def try_to_enable_start_button(self):
        if(self.serial_monitor.is_fully_connected and self.test_stand.current_state == self.test_stand_standby_state and self.config_is_loaded):
            self.start_button_enabled = True
        else:
            self.start_button_enabled = False
