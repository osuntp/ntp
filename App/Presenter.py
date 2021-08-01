from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets
from UI.UI import UI
from Log import Log
import threading
import Config
import time

class Presenter:
    def __init__(self, ui: UI):
        self.ui = ui

        self.__setup_functionality()
    
    def __setup_functionality(self):
        
        # This isn't working in a for loop for some reason, might be because of the lambda expression? revisit
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

    def tab_clicked(self, tab_index):
        Log.debug('A tab was clicked: This is a new test of the logging system. This system will be implemented in all classes going forward')

        if(self.ui.current_tab == self.ui.tabs[tab_index]):
            return

        self.ui.set_current_tab(tab_index)

    # TODO: Define abort procedure
    def abort_clicked(self):
        print('abort clicked')

    def configuration_blue_lines_plus_clicked(self):
        self.ui.configuration.add_row_to_blue_lines_table()
    def configuration_blue_lines_minus_clicked(self):
        self.ui.configuration.remove_row_from_blue_lines_table()
    
    def configuration_sequence_plus_clicked(self):
        self.ui.configuration.add_row_to_sequence_table()
    def configuration_sequence_minus_clicked(self):
        self.ui.configuration.remove_row_from_sequence_table()

    def configuration_save_clicked(self):
        self.my_thread = Config.ValidationThread(self.ui)

        self.my_thread.validation_message.connect(self.on_configuration_validation_message)
        self.my_thread.validation_is_complete.connect(self.on_configuration_validation_is_complete)

        self.my_thread.start()

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