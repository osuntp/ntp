
from configparser import ConfigParser
from dataclasses import dataclass
from enum import Enum
from PyQt5 import QtWidgets

@dataclass
class Config:
    trial_name: str
    description: str
    blue_lines: dict

def create():
    pass

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

def create_blue_line_dict(time_step: float, temp: float, is_max: str):
    return_dict = {
        'Timestep' : time_step,
        'Temperature' : temp,
        'Limit': is_max
    }

    return return_dict



if __name__ == "__main__":

    pass



# config = ConfigParser()
# config.add_section('main')
# config.set('main','key1','1')
# config.set('main','key2','2')
# config.set('main','key3','3')
# config.set('main','key4','4')

# with open('config.ini', 'w') as f:
#     config.write(f)

# config.read('config.ini')

# value1 = config.get('main', 'key1')

# a_float = config.getfloat('main','key1')

# print('a_float says ' + str(a_float))