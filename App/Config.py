from PyQt5.QtCore import QObject, QThread, pyqtSignal
from configparser import ConfigParser
from dataclasses import dataclass
from PyQt5 import QtWidgets
from typing import List
import time
import os

@dataclass
class Config:
    profile_name: str
    trial_name: str
    description: str

    blue_lines_time_step: List[float]
    blue_lines_sensor_type: List[str]
    blue_lines_limit_type: List[str]
    blue_lines_value: List[float]

    sequence_values: List

def create_file(file_name: str, profile_name:str, trial_name:str, description:str, blue_lines: QtWidgets.QTableWidget, num_of_test_sequence_var:int, test_sequence: QtWidgets.QTableWidget):
    config = ConfigParser()

    config.add_section('main')
    config.add_section('blue_lines')
    config.add_section('test_sequence')

    config.set('main', 'profile_name', profile_name)
    config.set('main','trial_name', trial_name)
    config.set('main', 'description', description)

# Blue Lines Data
    time_step = ''
    sensor_type = ''
    value = ''
    limit_type = ''

    for i in range(blue_lines.rowCount()):

        time_step += (str(blue_lines.item(i,0).text()))
        sensor_type += (str(blue_lines.cellWidget(i,1).currentText()))
        limit_type += blue_lines.cellWidget(i, 2).currentText()
        try:
            value += (str(blue_lines.item(i, 3).text()))
        except AttributeError:
            value = str(0)

        if(i < (blue_lines.rowCount() - 1)):
            time_step += ', '
            sensor_type += ', '
            limit_type +=', '
            value += ', '     

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

    profile_name = parser.get('main', 'profile_name')
    trial_name = parser.get('main', 'trial_name')
    description = parser.get('main','description')

    blue_lines_time_step = parser.get('blue_lines', 'time_step').split(sep = ', ')
    blue_lines_sensor_type = parser.get('blue_lines', 'sensor_type').split(sep = ', ')
    blue_lines_value = parser.get('blue_lines', 'value').split(sep = ', ')
    blue_lines_limit_type = parser.get('blue_lines', 'limit_type').split(sep=', ')

    if(blue_lines_time_step[0] == ''):
        blue_lines_time_step = []
        blue_lines_sensor_type = []
        blue_lines_value = []
        blue_lines_limit_type = []

    blue_lines_time_step = [float(x) for x in blue_lines_time_step]
    blue_lines_value = [float(x) for x in blue_lines_value]

    sequence_values = []

    for i in range(num_of_sequence_columns):
        id_string = 'value' + str(i)

        values = parser.get('test_sequence', id_string).split(sep = ', ')

        values = [float(x) for x in values]
        sequence_values.append(values)

    return Config(profile_name, trial_name, description, blue_lines_time_step, blue_lines_sensor_type, blue_lines_limit_type, blue_lines_value, sequence_values)