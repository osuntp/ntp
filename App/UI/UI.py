
from PyQt5.QtGui import QBrush, QColor, QPalette
from numpy import vdot
from UI.QT5_Generated_UI import Ui_window
from UI.Stylize import Stylize

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
import os

class UI:
    def __init__(self, window):       

        # [DO NOT EDIT]: this method is created by pyuic5.exe:
        self.pyqt5 = Ui_window()
        self.pyqt5.setupUi(window)
        # [END OF DO NOT EDIT]

        self.tabs_widget = self.pyqt5.stacked_widget
        self.tabs = [self.pyqt5.diagnostics_tab, self.pyqt5.logs_tab, self.pyqt5.manual_control_tab, self.pyqt5.configuration_tab, self.pyqt5.run_tab]
        self.current_tab = self.pyqt5.diagnostics_tab
        self.abort_tab = self.pyqt5.abort_tab

        Stylize.all_tabs(self.tabs)
        self.current_tab = self.tabs[1]
        self.set_current_tab(0)
        Stylize.abort(self.abort_tab)

        self.diagnostics = Diagnostics(self.pyqt5)
        self.logs = Logs(self.pyqt5)
        self.configuration = Configuration(self.pyqt5)
        self.run = Run(self.pyqt5)

    def set_current_tab(self, tab_index):
        new_tab = self.tabs[tab_index]
        prev_tab = self.current_tab

        Stylize.set_current_tab(new_tab, prev_tab)

        self.tabs_widget.setCurrentIndex(tab_index)

        self.current_tab = new_tab

    def set_hot_stand_status_light_is_lit(self, isLit: bool):
        Stylize.set_status_light_is_lit(self.side_bar_hot_stand_status, isLit)
    
    def set_valve_open_status_light_is_lit(self, isLit: bool):
        Stylize.set_status_light_is_lit(self.side_bar_valve_open_status, isLit)
    
    def set_heater_status_light_is_lit(self, isLit: bool):
        Stylize.set_status_light_is_lit(self.side_bar_heater_status, isLit)

class Diagnostics:
    def __init__(self, pyqt5:Ui_window):
        self.plot1 = Canvas(pyqt5.diagnostics_plot1, 'Time (s)', 'Temperature (C)')
        self.plot2 = Canvas(pyqt5.diagnostics_plot2, 'Time (s)', 'Pressure (Pa)')

        self.test_stand_status = pyqt5.diagnostics_state_value
        self.valve_voltage = pyqt5.diagnostics_r01_value
        self.mass_flow = pyqt5.diagnostics_r02_value
        self.heater_current = pyqt5.diagnostics_r03_value
        self.heater_duty_cycle = pyqt5.diagnostics_r04_value
        self.heater_power = pyqt5.diagnostics_r05_value
        self.heater_state = pyqt5.diagnostics_r06_value
        self.heater_set_point = pyqt5.diagnostics_r07_value

    def update_plots(self, diagnostics_dataframe):
        self.plot1.update_vals(diagnostics_dataframe['column1'], diagnostics_dataframe['column2'])

    def set_test_stand_status(self, value: float):
        self.test_stand_status.setText(str(value))

    def set_valve_voltage(self, value: float):
        self.valve_voltage.setText(str(value))

    def set_mass_flow(self, value: float):
        self.mass_flow.setText(str(value))

    def set_heater_current(self, value: float):
        self.heater_current.setText(str(value))

    def set_heater_duty_cycle(self, value: float):
        self.heater_duty_cycle.setText(str(value))

    def set_heater_power(self, value: float):
        self.heater_power.setText(str(value))

    def set_heater_state(self, value: str):
        self.heater_state.setText(value)

    def set_heater_set_point(self, value: float):
        self.heater_set_point.setText(str(value))

class Logs:
    def __init__(self, pyqt5: Ui_window):
        self.python = pyqt5.logs_python_log

    def update_python_log(self):
        path = os.getcwd()
        path = path + "\\app.log"

        with open(path, 'r') as file:
            data_list = file.readlines()
            data = ""

            for line in data_list:
                data += line + "<br><br>"
            self.python.setHtml(data)

class Configuration:
    def __init__(self, pyqt5: Ui_window):
        self.trial_name_field = pyqt5.configuration_trialname_field
        self.description_field = pyqt5.configuration_description_field

        self.blue_lines_table = pyqt5.configuration_blue_lines_table
        self.blue_lines_plus_button = pyqt5.configuration_blue_lines_plus
        self.blue_lines_minus_button = pyqt5.configuration_blue_lines_minus

        self.sequence_table = pyqt5.configuration_sequence_table
        self.sequence_plus_button = pyqt5.configuration_sequence_plus
        self.sequence_minus_button = pyqt5.configuration_sequence_minus

        self.status = pyqt5.configuration_status_label
        self.clear_button = pyqt5.configuration_clear_button
        self.save_button = pyqt5.configuration_save_button

        buttons = [self.save_button, self.clear_button, self.blue_lines_plus_button, self.blue_lines_minus_button, self.sequence_plus_button, self.sequence_minus_button]
        Stylize.button(buttons)

        self.clear_all()
        self.add_row_to_blue_lines_table()

    def add_row_to_blue_lines_table(self):
        table = self.blue_lines_table
        row_count = table.rowCount()
        column_count = table.columnCount()
        combo_box_options = ['Min', 'Max']    
        combo = QtWidgets.QComboBox()

        # if((row_count % 2) == 0):

        #     combo.setStyleSheet('border: 0px; background-color: rgb(206, 211, 230);')
        # else:
        #     combo.setStyleSheet('border: 0px; background-color: rgb(229, 231, 240);')

        for option in combo_box_options:
            combo.addItem(option)

        table.insertRow(row_count)
        table.setCellWidget(row_count, 2, combo)

        Stylize.table(table)

    def remove_row_from_blue_lines_table(self):
        table = self.blue_lines_table
        row_count = table.rowCount()

        if(row_count - 1 < 0.5):
            return

        table.removeRow(row_count - 1)

    def add_row_to_sequence_table(self):
        table = self.sequence_table
        row_count = table.rowCount()
        column_count = table.columnCount()

        table.insertRow(row_count)

    def remove_row_from_sequence_table(self):
        table = self.sequence_table
        row_count = table.rowCount()

        if(row_count - 1 < 0.5):
            return

        table.removeRow(row_count - 1)

    def set_status_text(self, text: str):
        self.status.setText(text)

    def clear_all(self):
        self.clear_blue_line_table()
        self.clear_sequence_table()

        self.status.setText('')

    def clear_blue_line_table(self):
        table = self.blue_lines_table

        while(table.rowCount() > 0.5):
            table.removeRow(table.rowCount() - 1)

        # Result will be 1 empty row
        self.add_row_to_blue_lines_table

    def clear_sequence_table(self):
        table = self.sequence_table

        while(table.rowCount() > 0.5):
            table.removeRow(table.rowCount() - 1)

        # Result will be 1 empty row
        self.add_row_to_sequence_table()
    
class Run:
    def __init__(self, pyqt5: Ui_window):
        self.load_button = pyqt5.run_load_configuration_button
        self.start_button = pyqt5.run_start_button
        self.loaded_trial_text = pyqt5.run_trialname

        Stylize.button([self.load_button])
        Stylize.set_start_button_active(self.start_button, False)

    def set_start_button_active(self, isActive: bool):
        Stylize.set_start_button_active(self.start_button, isActive)

    def set_loaded_trial_text(self, text: str):
        self.loaded_trial_text.setText(text)
            

class Canvas(FigureCanvas):
    def __init__(self, parent, xlabel, ylabel):
        self.fig, self.ax = plt.subplots(figsize=(5.67,2.76), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)

        self.xlabel = xlabel
        self.ylabel = ylabel

        self.__set_format()

    def update_vals(self, x, y):
        self.ax.cla()
        
        self.ax.plot(x,y)

        self.__set_format()
        
        self.draw()

    def __set_format(self):
        self.ax.set_xticks([0,1,2,3,4,5])
        self.ax.set_yticks([0,1,2,3,4,5,6,7,8,9,10])
        plt.subplots_adjust(bottom = 0.2)
        self.ax.set_xlim(0, 5)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylim(0,10)
        self.ax.set_ylabel(self.ylabel)
        self.ax.margins(0)
        self.ax.grid()