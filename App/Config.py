from PyQt5.QtCore import QObject, QThread, pyqtSignal
from configparser import ConfigParser
from dataclasses import dataclass
from PyQt5 import QtWidgets
from typing import List
import time
import os

@dataclass
class Config:
    trial_name: str
    description: str

    blue_lines_time_step: List[float]
    blue_lines_temperature: List[float]
    blue_lines_limit_type: List[str]

    sequence_time_step: List[float]
    sequence_power: List[float]
    sequence_temperature: List[float]
    sequence_mass_flow: List[float]

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
    config.set('main', 'description', description)

# Blue Lines Data
    time_step = ''
    temperature = ''
    limit_type = ''
    for i in range(blue_lines.rowCount()):

        time_step += (str(blue_lines.item(i,0).text()))
        temperature += (str(blue_lines.item(i, 1).text()))
        limit_type += blue_lines.cellWidget(i, 2).currentText()

        if(i < (blue_lines.rowCount() - 1)):
            time_step += ', '
            temperature += ', '
            limit_type +=', '

    
    config.set('blue_lines', 'time_step', time_step)
    config.set('blue_lines', 'temperature', temperature)
    config.set('blue_lines', 'limit_type', limit_type)

# Test Sequence Data
    time_step = ''
    power = ''
    temperature = ''
    mass_flow = ''

    for i in range(test_sequence.rowCount()):
        time_step += (str(test_sequence.item(i,0).text()))
        power += (str(test_sequence.item(i, 1).text()))
        temperature += (str(test_sequence.item(i, 2).text()))
        mass_flow += (str(test_sequence.item(i, 3).text()))

        if(i < (test_sequence.rowCount() - 1)):
            time_step += ', '
            power += ', '
            temperature += ', '
            mass_flow += ', '

    config.set('test_sequence', 'time_step', time_step)
    config.set('test_sequence', 'power', power)
    config.set('test_sequence', 'temperature', temperature)
    config.set('test_sequence', 'mass_flow', mass_flow)
    
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
    parser = ConfigParser()
    parser.read(file_name)

    trial_name = parser.get('main', 'trial_name')
    description = parser.get('main','description')

    blue_lines_time_step = parser.get('blue_lines', 'time_step').split(sep = ', ')
    blue_lines_temperature = parser.get('blue_lines', 'temperature').split(sep = ', ')
    blue_lines_limit_type = parser.get('blue_lines', 'limit_type').split(sep=', ')

    blue_lines_time_step = [float(x) for x in blue_lines_time_step]
    blue_lines_temperature = [float(x) for x in blue_lines_temperature]

    sequence_time_step = parser.get('test_sequence', 'time_step').split(sep = ', ')
    sequence_power = parser.get('test_sequence', 'power').split(sep = ', ')
    sequence_temperature = parser.get('test_sequence', 'temperature').split(sep = ', ')
    sequence_mass_flow = parser.get('test_sequence', 'mass_flow').split(sep = ', ')

    sequence_time_step = [float(x) for x in sequence_time_step]
    sequence_power = [float(x) for x in sequence_power]
    sequence_temperature = [float(x) for x in sequence_temperature]
    sequence_mass_flow = [float(x) for x in sequence_mass_flow]

    return Config(trial_name, description, blue_lines_time_step, blue_lines_temperature, blue_lines_limit_type, sequence_time_step, sequence_power, sequence_temperature, sequence_mass_flow)
    
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

