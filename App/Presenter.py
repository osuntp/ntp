import Model
import SM
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets
from UI import UI
from Log import Log
import threading
import Config
import time

class Presenter:

    ui: UI.UI = None
    model: Model.Model = None
    serial_monitor: SM.SerialMonitor = None
    def __init__(self):
        pass
    
    def setup(self):
        
        # TODO: This isn't working in a for loop for some reason, might be because of the lambda expression? revisit
        self.ui.tabs[0].clicked.connect(lambda: self.tab_clicked(0))
        self.ui.tabs[1].clicked.connect(lambda: self.tab_clicked(1))
        self.ui.tabs[2].clicked.connect(lambda: self.tab_clicked(2))
        self.ui.tabs[3].clicked.connect(lambda: self.tab_clicked(3))
        self.ui.tabs[4].clicked.connect(lambda: self.tab_clicked(4))

        # Abort
        self.ui.abort_tab.clicked.connect(self.abort_clicked)

        self.ui.configuration.blue_lines_plus_button.clicked.connect(self.configuration_blue_lines_plus_clicked)
        self.ui.configuration.blue_lines_minus_button.clicked.connect(self.configuration_blue_lines_minus_clicked)

        self.ui.configuration.sequence_plus_button.clicked.connect(self.configuration_sequence_plus_clicked)
        self.ui.configuration.sequence_minus_button.clicked.connect(self.configuration_sequence_minus_clicked)

        self.ui.configuration.save_button.clicked.connect(self.configuration_save_clicked)

        self.ui.run.load_button.clicked.connect(self.run_load_clicked)

        self.__start_ui_update_loop()

    def __start_ui_update_loop(self):
        self.ui_update_thread = UI.UpdateThread()
        self.ui_update_thread.set_max_frequency(1)
        self.ui_update_thread.update_signal.connect(self.on_ui_update)
        self.ui_update_thread.start()

    def on_ui_update(self):
        temperature = self.model.get_ui_data('Temperature')
        plot_time = self.model.get_ui_data('Time')
        max_value = max(plot_time)
        for i in range(len(plot_time)):
            plot_time[i] -= max_value
            plot_time[i] = plot_time[i] / 1000 #convert from milliseconds to seconds

        self.ui.run.plot1.update_vals(plot_time, temperature)

        self.ui.set_heater_status_light_is_lit(self.model.heater_is_on)

        self.ui.run.sequence_table_label.setText('Test Sequence - ' + str(round(self.model.time / 1000,1)))


    def tab_clicked(self, tab_index):
        if(self.ui.current_tab == self.ui.tabs[tab_index]):
            return

        self.ui.set_current_tab(tab_index)

    # TODO: Define abort procedure
    def abort_clicked(self):
        pass
        # self.serial_monitor.stop_collection_loop()


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
        pass

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

            if(file_name == ""):
                return

            trial_name = self.ui.configuration.trial_name_field.text()
            description = self.ui.configuration.description_field.toPlainText()
            blue_lines = self.ui.configuration.blue_lines_table
            test_sequence = self.ui.configuration.sequence_table
            
            Config.create_file(file_name, trial_name, description, blue_lines, test_sequence)

# RUN PAGE LOGIC
    def run_load_clicked(self):
        file_name = Config.select_file()
        
        if(file_name == ''):
            return

        config: Config.Config = Config.open_file(file_name)
        
        self.ui.run.set_loaded_trial_text(config.trial_name)
        self.ui.run.set_start_button_active(True)
        self.ui.run.set_sequence_table(config)