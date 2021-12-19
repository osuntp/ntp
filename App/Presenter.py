from StateMachine import TestStand
from StateMachine import TestStandStates
import Model
import SM
from PyQt5 import QtWidgets
from UI import UI
from Log import Log
import time
import Config
from UI.Stylize import Stylize
from SettingsManager import SettingsManager

class Presenter:

    app: QtWidgets.QApplication = None
    ui: UI.UI = None
    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None
    test_stand: TestStand.TestStand = None
    test_stand_standby_state: TestStandStates.StandbyState
    test_stand_trial_running_state: TestStandStates.TrialRunningState
    test_stand_trial_ended_state: TestStandStates.TrialEndedState
    test_stand_connecting_state: TestStandStates.ConnectingState

    def __init__(self):
        pass
    
    def setup(self):
        
        # TODO: This isn't working in a for loop for some reason, might be because of the lambda expression? revisit
        self.ui.tabs[0].clicked.connect(lambda: self.tab_clicked(0))
        self.ui.tabs[1].clicked.connect(lambda: self.tab_clicked(1))
        self.ui.tabs[2].clicked.connect(lambda: self.tab_clicked(2))
        self.ui.tabs[3].clicked.connect(lambda: self.tab_clicked(3))
        self.ui.tabs[4].clicked.connect(lambda: self.tab_clicked(4))
        self.ui.tabs[5].clicked.connect(lambda: self.tab_clicked(5))

        # Setup
        self.ui.setup.manual_connect_button.clicked.connect(self.setup_manual_connect_clicked)
        self.ui.setup.test_stand_behaviour_field.activated.connect(self.setup_behaviour_change_clicked)
        self.ui.setup.developer_mode_field.clicked.connect(self.setup_developer_mode_clicked)

        # Abort
        self.ui.abort_tab.clicked.connect(self.abort_clicked)

        # Manual
        self.ui.manual.send_valve_command_button.clicked.connect(self.manual_send_valve_command_clicked)
        self.ui.manual.send_heater_command_button.clicked.connect(self.manual_send_heater_command_clicked)

        # Configuration
        self.ui.configuration.blue_lines_plus_button.clicked.connect(self.configuration_blue_lines_plus_clicked)
        self.ui.configuration.blue_lines_minus_button.clicked.connect(self.configuration_blue_lines_minus_clicked)

        self.ui.configuration.sequence_plus_button.clicked.connect(self.configuration_sequence_plus_clicked)
        self.ui.configuration.sequence_minus_button.clicked.connect(self.configuration_sequence_minus_clicked)

        self.ui.configuration.save_button.clicked.connect(self.configuration_save_clicked)
        self.ui.configuration.clear_button.clicked.connect(self.configuration_clear_clicked)

        

        # Run
        self.ui.run.load_button.clicked.connect(self.run_load_clicked)
        self.ui.run.pause_button.clicked.connect(self.run_paused_clicked)
        self.ui.run.start_button.clicked.connect(self.run_start_clicked)

        self.ui.run.plot1_apply_buffer_button.clicked.connect(lambda: self.run_plot_apply_buffer_clicked(1))
        self.ui.run.plot2_apply_buffer_button.clicked.connect(lambda: self.run_plot_apply_buffer_clicked(2))
        self.ui.run.plot3_apply_buffer_button.clicked.connect(lambda: self.run_plot_apply_buffer_clicked(3))
        self.ui.run.plot4_apply_buffer_button.clicked.connect(lambda: self.run_plot_apply_buffer_clicked(4))

        self.ui.run.plot1_buffer_field.returnPressed.connect(lambda: self.run_plot_apply_buffer_clicked(1))
        self.ui.run.plot2_buffer_field.returnPressed.connect(lambda: self.run_plot_apply_buffer_clicked(2))
        self.ui.run.plot3_buffer_field.returnPressed.connect(lambda: self.run_plot_apply_buffer_clicked(3))
        self.ui.run.plot4_buffer_field.returnPressed.connect(lambda: self.run_plot_apply_buffer_clicked(4))


        # Start UI Update Loop
        self.__start_ui_update_loop()

    def __start_ui_update_loop(self):
        self.ui_update_thread = UI.UpdateThread()
        self.ui_update_thread.set_max_frequency(0.5)
        self.ui_update_thread.update_signal.connect(self.on_ui_update)
        self.ui_update_thread.start()

    def on_ui_update(self):
        
        if(self.ui.side_bar_valve_open_is_lit and self.test_stand.valve_position == 90):
            self.ui.set_valve_open_status_light_is_lit(True)
        elif(not self.ui.side_bar_valve_open_is_lit and self.test_stand.valve_position != 90):
            self.ui.set_valve_open_status_light_is_lit(False)

        if(self.ui.side_bar_state_text != self.model.state_text):
            self.ui.set_side_bar_state_text(self.model.state_text)

        page = self.ui.pyqt5.stacked_widget.currentIndex()

        # 5 - Setup
        # 0 - Diagnostics
        # 1 - Logs
        # 2 - Manual
        # 3 - Config
        # 4 - Run

        # Setup Page
        if(page == 5):
            self.ui.setup.daq_status_label.setText(self.model.daq_status_text)
            self.ui.setup.controller_status_label.setText(self.model.tsc_status_text)

            self.ui.setup.manual_connect_button.setEnabled(self.model.connect_arduinos_button_enabled)

        # Diagnostics Page
        if(page == 0):
            # TODO: Implement diagnostics UI update logic
            pass
        
        # Logs Page
        if(page == 1):
            self.ui.logs.update_python_log(Log.file_path)

        # Manual Page
        if(page == 2):
            self.ui.manual.set_command_buttons_active(not self.model.trial_is_running)

            # TODO: Update manual control page
            # self.ui.currentValvePosLabel.setText(_translate("MainWindow","Current: <valve pos> "))
            # self.ui.currentHeaterLabel.setText(_translate("MainWindow","Current: <heater power> "))

        # Configuration Page
        if(page == 3):
            pass

        if(page == 4):
            self.ui.run.start_button.setText(self.model.start_button_text)

            if(self.model.run_sequence_bolded_row != self.ui.run.sequence_table_bold_row):
                
                self.ui.run.set_sequence_table_row_bold(self.model.run_sequence_bolded_row)

            # Update Plot1
            if(self.ui.run.plot1_inlet_check.isChecked()):
                x, y = self.model.get_run_plot_data('Inlet TC')
                self.ui.run.plot1_inlet.setData(x,y)
            else:
                self.ui.run.plot1_inlet.setData([0],[0])

            if(self.ui.run.plot1_midpoint_check.isChecked()):
                x, y = self.model.get_run_plot_data('Midpoint TC')
                self.ui.run.plot1_midpoint.setData(x,y)
            else:
                self.ui.run.plot1_midpoint.setData([0],[0])

            if(self.ui.run.plot1_outlet_check.isChecked()):
                x, y = self.model.get_run_plot_data('Outlet TC')
                self.ui.run.plot1_outlet.setData(x,y)
            else:
                self.ui.run.plot1_outlet.setData([0],[0])

            if(self.ui.run.plot1_heat_sink_check.isChecked()):
                x, y = self.model.get_run_plot_data('Flow Temperature')
                self.ui.run.plot1_heat_sink.setData(x,y)
            else:
                self.ui.run.plot1_heat_sink.setData([0],[0])

            # Update Plot2
            if(self.ui.run.plot2_inlet_check.isChecked()):
                x, y = self.model.get_run_plot_data('Inlet Pressure')
                self.ui.run.plot2_inlet.setData(x,y)
            else:
                self.ui.run.plot2_inlet.setData([0],[0])

            if(self.ui.run.plot2_midpoint_check.isChecked()):
                x, y = self.model.get_run_plot_data('Midpoint Pressure')
                self.ui.run.plot2_midpoint.setData(x,y)
            else:
                self.ui.run.plot2_midpoint.setData([0],[0])

            if(self.ui.run.plot2_outlet_check.isChecked()):
                x, y = self.model.get_run_plot_data('Outlet Pressure')
                self.ui.run.plot2_outlet.setData(x,y)
            else:
                self.ui.run.plot2_outlet.setData([0],[0])

            if(self.ui.run.plot2_tank_check.isChecked()):
                x, y = self.model.get_run_plot_data('Tank Pressure')
                self.ui.run.plot2_tank.setData(x,y)
            else:
                self.ui.run.plot2_tank.setData([0],[0])

            # Update Plot3
            x, y = self.model.get_run_plot_data('Mass Flow')
            # print(x)
            # print(y)
            self.ui.run.plot3_mass_flow.setData(x,y)

            # Update Plot4
            if(self.ui.run.plot4_valve_position_check.isChecked()):
                x, y = self.model.get_run_plot_data('Valve Position')
                self.ui.run.plot4_valve_position.setData(x,y)
            else:
                self.ui.run.plot4_valve_position.setData([0],[0])

            if(self.ui.run.plot4_heater_duty_check.isChecked()):
                x, y = self.model.get_run_plot_data('Heater Status')
                self.ui.run.plot4_heater_duty.setData(x,y)
            else:
                self.ui.run.plot4_heater_duty.setData([0],[0])

            if(self.ui.run.plot4_openfoam_check.isChecked()):
                x, y = self.model.get_run_plot_data('OpenFOAM Progress')
                self.ui.run.plot4_openFOAM.setData(x,y)
            else:
                self.ui.run.plot4_openFOAM.setData([0],[0])

        # Update status lights on left columns
        # if any temp is above 80 deg. F, "Hot Stand" should be on
        # if valve position is not 90 degrees, "Valve Open" should be on
        # if heater is on, "Heater On" should be on

    def tab_clicked(self, tab_index):
        if(self.ui.current_tab == self.ui.tabs[tab_index]):
            return

        self.ui.set_current_tab(tab_index)

    # TODO: Define abort procedure
    def abort_clicked(self):
            print('Abort was pressed but this functionality has not been implemented.')

# SETUP PAGE LOGIC
    def setup_manual_connect_clicked(self): 
        daq_port = self.ui.setup.daq_port_field.text()
        tsc_port = self.ui.setup.controller_port_field.text()

        SettingsManager.save_arduino_ports(daq_port, tsc_port)

        self.test_stand_connecting_state.daq_port = daq_port
        self.test_stand_connecting_state.tsc_port = tsc_port

        self.test_stand.switch_state(self.test_stand_connecting_state)

    def setup_behaviour_change_clicked(self):
        i = self.ui.setup.test_stand_behaviour_field.currentIndex()

        self.model.config_is_loaded = False
        self.run_attempt_to_activate_start_button()
        self.test_stand.set_profile(i)
        SettingsManager.save_profile_index(i)

    def setup_developer_mode_clicked(self):

        is_checked = self.ui.setup.developer_mode_field.isChecked()
        self.serial_monitor.set_developer_mode(is_checked)
        SettingsManager.save_developer_mode(is_checked)

        self.model.connect_arduinos_button_enabled = not is_checked

# MANUAL PAGE LOGIC
    def manual_send_valve_command_clicked(self):
        value = self.ui.manual.valve_field.value()

        if(value>=0 and value<=90):
            self.ui.manual.current_valve_position_label.setText('Current: ' + str(value))
            self.test_stand.set_valve_position(value)

    def manual_send_heater_command_clicked(self):
        pass

# CONFIGURATION PAGE LOGIC
    def configuration_blue_lines_plus_clicked(self):
        self.ui.configuration.add_row_to_blue_lines_table()
    def configuration_blue_lines_minus_clicked(self):
        self.ui.configuration.remove_row_from_blue_lines_table()
    
    def configuration_sequence_plus_clicked(self):
        self.ui.configuration.add_row_to_sequence_table()
    def configuration_sequence_minus_clicked(self):
        self.ui.configuration.remove_row_from_sequence_table()

    def configuration_clear_clicked(self):
        self.ui.configuration.clear_all()

    def configuration_save_clicked(self):
        file_name = Config.get_save_file_name_from_user()

        if(file_name == ''):
            return

        profile_name = self.test_stand_trial_running_state.current_profile.name
        trial_name = self.ui.configuration.trial_name_field.text()
        description = self.ui.configuration.description_field.toPlainText()
        blue_lines = self.ui.configuration.blue_lines_table
        num_of_test_sequence_var = len(self.test_stand_trial_running_state.current_profile.columns)
        test_sequence = self.ui.configuration.sequence_table
        trial_end_timestep = self.ui.configuration.trial_end_timestep_field.text()
        
        Config.create_file(file_name, profile_name, trial_name, description, blue_lines, num_of_test_sequence_var, test_sequence, trial_end_timestep)

        # TODO: Validation was removed, consider if it needs added again
        # self.config_validation_thread = Config.ValidationThread(self.ui)

        # self.config_validation_thread.validation_message.connect(self.on_configuration_validation_message)
        # self.config_validation_thread.validation_is_complete.connect(self.on_configuration_validation_is_complete)

        # self.config_validation_thread.start()

    # def on_configuration_validation_message(self, message):
    #     self.ui.configuration.set_status_text(message)

    # def on_configuration_validation_is_complete(self, validation_was_successful):
    #     if(validation_was_successful):
    #         file_name = Config.get_save_file_name_from_user()

    #         if(file_name == ''):
    #             return

    #         trial_name = self.ui.configuration.trial_name_field.text()
    #         description = self.ui.configuration.description_field.toPlainText()
    #         blue_lines = self.ui.configuration.blue_lines_table
    #         test_sequence = self.ui.configuration.sequence_table
    #         trial_end_timestep = self.ui.configuration.trial_end_timestep_field.text()
            
    #         Config.create_file(file_name, trial_name, description, blue_lines, test_sequence, trial_end_timestep)

    def run_attempt_to_activate_start_button(self):
        # TODO: Replace this method logic with the commented code below:
        if(self.model.config_is_loaded and self.serial_monitor.is_fully_connected):
            self.ui.run.set_start_button_clickable(True)
        else:
            self.ui.run.set_start_button_clickable(False)
        # if(self.model.config_is_loaded):
        #     self.ui.run.set_start_button_clickable(True)
        # else:
        #     self.ui.run.set_start_button_clickable(False)

    def run_start_clicked(self):         
        self.test_stand.switch_state(self.test_stand_trial_running_state)


    def run_paused_clicked(self):
        Log.info('Trial has been stopped.')
        self.test_stand.switch_state(self.test_stand_trial_ended_state)    

    def run_load_clicked(self):
        

        file_name = Config.select_file()
        
        if(file_name == ''):
            return

        
        Log.info('Trial configuration has been loaded.')
        config: Config.Config = Config.open_file(file_name, len(self.test_stand_trial_running_state.current_profile.columns))

        current_profile_name = self.test_stand_trial_running_state.current_profile.name

        print(config.profile_name)
        print(current_profile_name)
        if(config.profile_name != current_profile_name):
            self.ui.run.set_loaded_trial_text('Invalid CONFIG File')
            
        else:


            self.model.config_is_loaded = True
            self.model.loaded_config_trial_name = config.trial_name

            self.ui.run.set_loaded_trial_text(config.trial_name)
            self.test_stand.end_trial_time = float(config.trial_end_timestep)
            self.test_stand_trial_running_state.current_profile.set_sequence_values(config.sequence_values)
            self.ui.run.set_sequence_table(config.sequence_values, self.test_stand.end_trial_time)
        
            self.run_attempt_to_activate_start_button()
    
    def run_plot_apply_buffer_clicked(self, plot_index):
        try:
            max_value = 90
            min_value = 1

            if(plot_index == 1):
                value = float(self.ui.run.plot1_buffer_field.text())

                if(value > max_value):
                    self.ui.run.plot1_buffer_field.setText(str(max_value))
                    value = max_value
                elif(value < min_value):
                    self.ui.run.plot1_buffer_field.setText(str(min_value))
                    value = min_value
                
                self.ui.run.plot1.setXRange(-1 * value, 0)
            elif(plot_index == 2):
                value = float(self.ui.run.plot2_buffer_field.text())
                if(value > max_value):
                    self.ui.run.plot2_buffer_field.setText(str(max_value))
                    value = max_value
                elif(value < min_value):
                    self.ui.run.plot2_buffer_field.setText(str(min_value))
                    value = min_value
                
                self.ui.run.plot2.setXRange(-1 * value, 0)
            elif(plot_index == 3):
                value = float(self.ui.run.plot3_buffer_field.text())
                if(value > max_value):
                    self.ui.run.plot3_buffer_field.setText(str(min_value))
                    value = max_value
                elif(value < min_value):
                    self.ui.run.plot3_buffer_field.setText(str(min_value))
                    value = min_value
                
                self.ui.run.plot3.setXRange(-1 * value, 0)
            elif(plot_index == 4):
                value = float(self.ui.run.plot4_buffer_field.text())
                if(value > max_value):
                    self.ui.run.plot4_buffer_field.setText(str(min_value))
                    value = max_value
                elif(value < min_value):
                    self.ui.run.plot4_buffer_field.setText(str(min_value))
                    value = min_value

                self.ui.run.plot4.setXRange(-1 * value, 0)
        except ValueError:
            return