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

class Presenter:

    app: QtWidgets.QApplication = None
    ui: UI.UI = None
    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None
    test_stand: TestStand.TestStand = None
    test_stand_standby_state: TestStandStates.DemoStandbyState
    test_stand_idle_state: TestStandStates.DemoIdleState
    test_stand_auto_state: TestStandStates.DemoAutoState

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

        # Abort
        self.ui.abort_tab.clicked.connect(self.abort_clicked)

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

        # Start UI Update Loop
        self.__start_ui_update_loop()

    def __start_ui_update_loop(self):
        self.ui_update_thread = UI.UpdateThread()
        self.ui_update_thread.set_max_frequency(0.5)
        self.ui_update_thread.update_signal.connect(self.on_ui_update)
        self.ui_update_thread.start()

    def on_ui_update(self):

        self.ui.setup.daq_status_label.setText(self.model.daq_status_text)
        self.ui.setup.controller_status_label.setText(self.model.controller_status_text)

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
            x, y = self.model.get_run_plot_data('Heater TC')
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


        # If Trial is running
        if(self.model.trial_is_running):
            self.ui.run.start_button.setText('Running Trial - ' + str(round(self.model.trial_time, 1)))

            next_index = self.model.current_trial_time_stamp_index + 1
            
            if next_index <= (len(self.model.loaded_config.sequence_time_step) - 1):
                if(self.model.trial_time > self.model.loaded_config.sequence_time_step[next_index]):
                    self.model.current_trial_time_stamp_index = next_index
                    self.ui.run.set_sequence_table_row_bold(next_index)

    def tab_clicked(self, tab_index):
        if(self.ui.current_tab == self.ui.tabs[tab_index]):
            return

        self.ui.set_current_tab(tab_index)

    # TODO: Define abort procedure
    def abort_clicked(self):
        if(self.model.trial_is_paused or self.model.trial_is_running):

            Log.info('ABORTING CURRENT TRIAL')
            Log.info('Saving ')
            self.ui.run.set_start_button_clickable(False)
            self.ui.run.set_pause_button_clickable(False)
            self.ui.set_abort_tab_clickable(False)

            self.test_stand.switch_state(self.test_stand_standby_state)
            self.ui.run.start_button.setText('Aborting.')
            self.app.processEvents()
            time.sleep(0.5)
            self.ui.run.start_button.setText('Aborting. .')
            self.app.processEvents()
            time.sleep(0.5)
            self.ui.run.start_button.setText('Aborting. . .')
            self.app.processEvents()
            time.sleep(0.5)
            self.ui.run.set_start_button_clickable(True)
            self.ui.set_abort_tab_clickable(True)
            self.ui.run.start_button.setText('Start')
            self.ui.run.set_sequence_table_row_bold(-1)
            self.model.save_trial_data(True)

# SETUP PAGE LOGIC

    def setup_manual_connect_clicked(self): 
        daq_port = self.ui.setup.daq_port_field.text()
        controller_port = self.ui.setup.controller_port_field.text()
        self.ui.setup.controller_status_label.setText('Attempting to Connect...')
        self.ui.setup.daq_status_label.setText('Attempting to Connect...')
        Stylize.set_button_active(self.ui.setup.manual_connect_button, False)
        self.ui.setup.manual_connect_button.setDisabled(True)
        self.app.processEvents()
        self.serial_monitor.connect_arduinos(daq_port, controller_port)
        Stylize.set_button_active(self.ui.setup.manual_connect_button, True)
        self.ui.setup.manual_connect_button.setDisabled(False)


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
        self.config_validation_thread = Config.ValidationThread(self.ui)

        self.config_validation_thread.validation_message.connect(self.on_configuration_validation_message)
        self.config_validation_thread.validation_is_complete.connect(self.on_configuration_validation_is_complete)

        self.config_validation_thread.start()

    def on_configuration_validation_message(self, message):
        self.ui.configuration.set_status_text(message)

    def on_configuration_validation_is_complete(self, validation_was_successful):
        if(validation_was_successful):
            file_name = Config.get_save_file_name_from_user()

            if(file_name == ''):
                return

            trial_name = self.ui.configuration.trial_name_field.text()
            description = self.ui.configuration.description_field.toPlainText()
            blue_lines = self.ui.configuration.blue_lines_table
            test_sequence = self.ui.configuration.sequence_table
            
            Config.create_file(file_name, trial_name, description, blue_lines, test_sequence)

# RUN PAGE LOGIC
    def run_start_clicked(self):
        if not(self.model.trial_is_paused):
            self.ui.run.set_sequence_table_row_bold(0)

        self.test_stand.switch_state(self.test_stand_auto_state)
        self.ui.run.set_start_button_clickable(False)
        self.ui.run.set_pause_button_clickable(True)

    def run_paused_clicked(self):
        print('pause button clicked')
        self.test_stand.switch_state(self.test_stand_idle_state)
        self.ui.run.set_start_button_clickable(True)
        self.ui.run.set_pause_button_clickable(False)
        self.ui.run.start_button.setText('Resume Trial at ' + str(round(self.model.trial_time,1)))

    def run_load_clicked(self):
        file_name = Config.select_file()
        
        if(file_name == ''):
            return

        config: Config.Config = Config.open_file(file_name)
        self.model.loaded_config = config
        self.ui.run.set_loaded_trial_text(config.trial_name)
        self.ui.run.set_start_button_clickable(True)
        self.ui.run.set_sequence_table(config)
