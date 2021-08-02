from PyQt5.QtCore import QObject, QThread, pyqtSignal
from configparser import ConfigParser
from dataclasses import dataclass
from PyQt5 import QtWidgets
import time
import os

@dataclass
class Config:
    trial_name: str
    description: str
    blue_lines: dict

class ValidationThread(QThread):

    validation_message = pyqtSignal(object)
    validation_is_complete = pyqtSignal(object)

    def __init__(self, ui):
        QThread.__init__(self)
        self.ui = ui

    def run(self):
        self.validation_message.emit('Validating.')
        time.sleep(0.25)
        self.validation_message.emit('Validating. .')
        time.sleep(0.25)
        self.validation_message.emit('Validating. . .')
        time.sleep(0.2)

        blue_lines_table = self.ui.configuration.blue_lines_table
        test_sequence_table = self.ui.configuration.sequence_table
        message = 'valid'

        if(message == 'valid'):
            message = blue_lines_is_valid(blue_lines_table)

        if(message == 'valid'):
            message = test_sequence_is_valid(test_sequence_table)

        if(message == 'valid'):
            message = 'Valid Configuration\nSaving to configuration file.'
            self.validation_message.emit(message)
            self.validation_is_complete.emit(True)
        else:
            message = 'INVALID CONFIGURATION\n' + message
            self.validation_message.emit(message)
            self.validation_is_complete.emit(False)

def create_file(file_name: str, trial_name:str, description:str, blue_lines: QtWidgets.QTableWidget, test_sequence: QtWidgets.QTableWidget):
    config = ConfigParser()

    config.add_section('main')
    config.add_section('blue_lines')
    config.add_section('test_sequence')

    config.set('main','trial_name', trial_name)
    config.set('main', 'decription', description)

    config.set('blue_lines', 'row_count', str(blue_lines.rowCount()))

    for i in range(blue_lines.rowCount()):
        time_step_id = "time_step_" + str(i)
        time_step_value = blue_lines.item(i,0).text()

        temperature_id = "temperature_"+str(i)
        temperature_value = blue_lines.item(i,1).text()

        limit_type_id = "limit_type_" + str(i)
        limit_type_value = blue_lines.cellWidget(i, 2).currentText()

        config.set('blue_lines', time_step_id, time_step_value)
        config.set('blue_lines', temperature_id, temperature_value)
        config.set('blue_lines', limit_type_id, limit_type_value)

    config.set('test_sequence', 'row_count', str(test_sequence.rowCount()))

    for i in range(test_sequence.rowCount()):
        time_step_id = "time_step_" + str(i)
        time_step_value = test_sequence.item(i,0).text()

        power_id = "power_" + str(i)
        power_value = test_sequence.item(i,1).text()

        temperature_id = "temperature_"+str(i)
        temperature_value = test_sequence.item(i,2).text()

        mass_flow_id = "mass_flow_" + str(i)
        mass_flow_value = test_sequence.item(i,3).text()

        config.set('test_sequence', time_step_id, time_step_value)
        config.set('test_sequence', power_id, power_value)
        config.set('test_sequence', temperature_id, temperature_value)
        config.set('test_sequence', mass_flow_id, mass_flow_value)
    
    with open(file_name, 'w') as f:
        config.write(f)

def get_save_file_name_from_user():
    file_dialog = QtWidgets.QFileDialog()
    file_filter = 'Config File (*.ini)'

    response = file_dialog.getSaveFileName(
        caption = 'Select a config file',
        directory = 'Config.ini',
        filter = file_filter,
        initialFilter = 'Config File (*.ini)'
    )

    return response[0]

def select_file():
    file_dialog = QtWidgets.QFileDialog()
    file_filter = 'Config File (*.ini)'

    response = file_dialog.getOpenFileName(
        caption = 'Select a config file',
        directory = os.getcwd(),
        filter = file_filter,
        initialFilter = 'Config File (*.ini)'
    )
    
    return response[0]

def open_file(file_name: str):
    config = ConfigParser()
    config.read(file_name)

    return config.get('main', 'trial_name')
    
def blue_lines_is_valid(table: QtWidgets.QTableWidget):
    
    previous_time_step = 0
    current_time_step = 0
    # Iterate over all rows in QTableWidget
    for i in range(table.rowCount()):

        # Determine if column 0 and 1 are numbers by trying to cast to float, if ValueError then there are illegal characters
        try:
            # Timestep logic
            previous_time_step = current_time_step

            if(table.item(i,0) is None):
                return 'One of the values in blue lines table is blank.'

            current_time_step = float(table.item(i,0).text())
           
            if((i > 0.5) and (current_time_step <= previous_time_step)):
                return 'The time steps in the blue lines table are out of order.'
            
            # Other
            float(table.item(i,1).text())

        except ValueError:
            return 'Invalid characters detected in test sequence table.'

    return 'valid'

def test_sequence_is_valid(table: QtWidgets.QTableWidget):
    previous_time_step = 0
    current_time_step = 0

    # Iterate over all rows in QTableWidget
    for i in range(table.rowCount()):

        # Determine if column 0, 1, and 2 are numbers by trying to cast to float, if ValueError then there are illegal characters
        try:
            # Timestep logic
            previous_time_step = current_time_step         
            current_time_step = float(table.item(i,0).text())
           
            if(table.item(i,0) is None):
                return 'One of the values in test sequence table is blank.'

            if((i > 0.5) and (current_time_step <= previous_time_step)):
                return 'The time steps in the test sequence table are out of order.'
            
            # Other
            float(table.item(i,1).text())
            float(table.item(i,2).text())
            
        except ValueError:
            return 'Invalid characters detected in test sequence table.'

    return 'valid'

