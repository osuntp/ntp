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
    trial_end_timestep: str

    blue_lines_time_step: List[float]
    blue_lines_sensor_type: List[str]
    blue_lines_limit_type: List[str]
    blue_lines_value: List[float]

    sequence_values: List
    # sequence_time_step: List[float]
    # sequence_power: List[float]
    # sequence_mass_flow_rate: List[float]
    # sequence_valve_position: List[float]
    # sequence_OF_instruction: List[float]

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

def create_file(file_name: str, trial_name:str, description:str, blue_lines: QtWidgets.QTableWidget, num_of_test_sequence_var:int, test_sequence: QtWidgets.QTableWidget, trial_end_timestep: str):
    config = ConfigParser()

    config.add_section('main')
    config.add_section('blue_lines')
    config.add_section('test_sequence')

    config.set('main','trial_name', trial_name)
    config.set('main', 'description', description)
    config.set('main', 'trial_end_timestep', trial_end_timestep)

# Blue Lines Data
    time_step = ''
    sensor_type = ''
    value = ''
    limit_type = ''

    for i in range(blue_lines.rowCount()):

        time_step += (str(blue_lines.item(i,0).text()))
        sensor_type += (str(blue_lines.cellWidget(i,1).currentText()))
        limit_type += blue_lines.cellWidget(i, 2).currentText()
        value += (str(blue_lines.item(i, 3).text()))

        if(i < (blue_lines.rowCount() - 1)):
            time_step += ', '
            value += ', '
            limit_type +=', '

    
    config.set('blue_lines', 'time_step', time_step)
    config.set('blue_lines', 'sensor_type', sensor_type)
    config.set('blue_lines', 'limit_type', limit_type)
    config.set('blue_lines', 'value', value)

# Test Sequence Data
    for i in range(num_of_test_sequence_var):

        test_sequence_values_string = ''

        for j in range(test_sequence.rowCount()):
            test_sequence_values_string += str(test_sequence.item(j,i).text())

            if(j < (test_sequence.rowCount() - 1)):
                test_sequence_values_string += ', '

        value_name = 'value' + str(i)
        config.set('test_sequence', value_name, test_sequence_values_string)

    # time_step = ''
    # power = ''
    # mass_flow_rate = ''
    # valve_position = ''
    # OF_instruction = ''

    # for i in range(test_sequence.rowCount()):
    #     time_step += (str(test_sequence.item(i,0).text()))
    #     power += (str(test_sequence.item(i, 1).text()))

    #     if(i < (test_sequence.rowCount() - 1)):
    #         time_step += ', '
    #         power += ', '
    #         mass_flow_rate += ', '
    #         valve_position += ', '
    #         OF_instruction += ', '

    # config.set('test_sequence', 'time_step', time_step)
    # config.set('test_sequence', 'power', power)
    # config.set('test_sequence', 'mass_flow_rate', mass_flow_rate)
    # config.set('test_sequence', 'valve_position', valve_position)
    # config.set('test_sequence', 'OF_instruction', OF_instruction)
    
    with open(file_name, 'w') as f:
        config.write(f)

def get_save_file_name_from_user():
    file_dialog = QtWidgets.QFileDialog()
    file_filter = 'Config File (*.ini)'

    cwd = os.getcwd()

    response = file_dialog.getSaveFileName(
        caption = 'Select a config file',
        directory = cwd + '\TrialConfigs\Config.ini',
        filter = file_filter,
        initialFilter = 'Config File (*.ini)'
    )

    return response[0]

def select_file():
    file_dialog = QtWidgets.QFileDialog()
    file_filter = 'Config File (*.ini)'

    cwd = os.getcwd()

    response = file_dialog.getOpenFileName(
        caption = 'Select a config file',
        directory = cwd + '\TrialConfigs\\',
        filter = file_filter,
        initialFilter = 'Config File (*.ini)'
    )
    
    return response[0]

def open_file(file_name: str, num_of_sequence_columns: int):
    parser = ConfigParser()
    parser.read(file_name)

    trial_name = parser.get('main', 'trial_name')
    description = parser.get('main','description')
    trial_end_timestep = parser.get('main', 'trial_end_timestep')

    blue_lines_time_step = parser.get('blue_lines', 'time_step').split(sep = ', ')
    blue_lines_sensor_type = parser.get('blue_lines', 'sensor_type').split(sep = ', ')
    blue_lines_value = parser.get('blue_lines', 'value').split(sep = ', ')
    blue_lines_limit_type = parser.get('blue_lines', 'limit_type').split(sep=', ')

    blue_lines_time_step = [float(x) for x in blue_lines_time_step]
    blue_lines_value = [float(x) for x in blue_lines_value]

    sequence_values = []

    for i in range(num_of_sequence_columns):
        id_string = 'value' + str(i)

        values = parser.get('test_sequence', id_string).split(sep = ', ')

        values = [float(x) for x in values]
        sequence_values.append(values)

    return Config(trial_name, description, trial_end_timestep, blue_lines_time_step, blue_lines_sensor_type, blue_lines_limit_type, blue_lines_value, sequence_values)


    # sequence_time_step = parser.get('test_sequence', 'time_step').split(sep = ', ')
    # sequence_power = parser.get('test_sequence', 'power').split(sep = ', ')
    # sequence_mass_flow_rate = parser.get('test_sequence', 'mass_flow_rate').split(sep = ', ')
    # sequence_valve_position = parser.get('test_sequence', 'valve_position').split(sep = ', ')
    # sequence_OF_instruction = parser.get('test_sequence', 'OF_instruction').split(sep = ', ')

    # sequence_time_step = [float(x) for x in sequence_time_step]
    # sequence_power = [float(x) for x in sequence_power]
    # sequence_mass_flow_rate = [float(x) for x in sequence_mass_flow_rate]
    # sequence_valve_position = [float(x) for x in sequence_valve_position]
    # sequence_OF_instruction = [float(x) for x in sequence_OF_instruction]

    # return config_values
    
def blue_lines_is_valid(table: QtWidgets.QTableWidget):
    
    previous_time_step = 0
    current_time_step = 0
    # Iterate over all rows in QTableWidget
    for i in range(table.rowCount()):

        # Determine if column 0 and 3 are numbers by trying to cast to float, if ValueError then there are illegal characters
        try:
            # Timestep logic
            previous_time_step = current_time_step

            if(table.item(i,0) is None):
                return 'One of the values in blue lines table is blank.'

            current_time_step = float(table.item(i,0).text())
           
            # TODO: Determine if we want to check for order of timesteps or not.
            # if((i > 0.5) and (current_time_step <= previous_time_step)):
            #     return 'The time steps in the blue lines table are out of order.'
            
            # Other
            float(table.item(i,3).text())

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
            # 1: mass flow
            # 2: heater
            # 3: valve
            # 4: OF instruction
            float(table.item(i,1).text())
            float(table.item(i,2).text())
            float(table.item(i,3).text())
            float(table.item(i,4).text())

            if bool(table.item(i,1).text() and table.item(i,3).text()):
                return 'Cannot prescribe mass flow and valve position.'

            
        except ValueError:
            return 'Invalid characters detected in test sequence table.'

    return 'valid'

