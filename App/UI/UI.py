
from UI.QT5_Generated_UI import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
# from UI.QT5_Generated_UI import Ui_window
from UI.Stylize import Stylize

# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
import os
import Config
import time

class Window(QMainWindow):
    pass

class UI:
    def __init__(self, window):       

        # [DO NOT EDIT]: this method is created by pyuic5.exe:
        self.pyqt5 = Ui_MainWindow()
        self.pyqt5.setupUi(window)
        # [END OF DO NOT EDIT]

        self.tabs_widget = self.pyqt5.stacked_widget
        self.tabs = [self.pyqt5.diagnostics_tab, self.pyqt5.logs_tab, self.pyqt5.manual_control_tab, self.pyqt5.configuration_tab, self.pyqt5.run_tab, self.pyqt5.setup_tab]
        self.current_tab = self.pyqt5.setup_tab
        self.abort_tab = self.pyqt5.abort_tab

        Stylize.all_tabs(self.tabs)
        Stylize.abort(self.abort_tab)

        self.current_tab = self.tabs[1]
        self.set_current_tab(5)

        self.side_bar_hot_stand_status = self.pyqt5.side_bar_hot_stand_status
        self.side_bar_heater_status = self.pyqt5.side_bar_heater_status
        self.side_bar_valve_open_status = self.pyqt5.side_bar_valve_open_status

        self.setup = Setup(self.pyqt5)
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
    def __init__(self, pyqt5:Ui_MainWindow):
        self.plot1 = pyqt5.diagnostics_plot1.getPlotItem()
        self.plot2 = pyqt5.diagnostics_plot2.getPlotItem()

        # self.plot1.set_labels('Time (s)', 'Temperature (C)')
        # self.plot2.set_labels('Time (s)', 'Pressure (Pa)')

# TODO: Remove this call to update_vals
        self.plot1.plot([0],[0])
        self.plot2.plot([0],[0])

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
    def __init__(self, pyqt5: Ui_MainWindow):
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
    def __init__(self, pyqt5: Ui_MainWindow):
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
    def __init__(self, pyqt5: Ui_MainWindow):
        self.load_button = pyqt5.run_load_configuration_button
        self.start_button = pyqt5.run_start_button
        self.pause_button = pyqt5.run_pause_button
        self.loaded_trial_text = pyqt5.run_trialname
        self.sequence_table = pyqt5.run_test_sequence_table
        self.sequence_table_label = pyqt5.run_test_sequence_label

        self.plot1 = pyqt5.run_plot1.getPlotItem().plot()
        pyqt5.run_plot1.setXRange(-10, 0)
        pyqt5.run_plot1.setYRange(0,1)
        # self.plot1.set_axis_labels('Time (s)', 'Temperature (C)')

        self.plot2 = pyqt5.run_plot2.getPlotItem().plot()
        pyqt5.run_plot2.setXRange(-10, 0)
        pyqt5.run_plot2.setYRange(0,1)
        # self.plot2.set_axis_labels('Time (s)', 'Pressure (Pa)')

        self.plot3 = pyqt5.run_plot3.getPlotItem().plot()
        pyqt5.run_plot3.setXRange(-10, 0)
        pyqt5.run_plot3.setYRange(0,1)
        # self.plot3.set_axis_labels('Time (s)', 'Mass Flow (kg/s)')

        self.plot4 = pyqt5.run_plot4.getPlotItem().plot()
        pyqt5.run_plot4.setXRange(-10, 0)
        pyqt5.run_plot4.setYRange(0,1)
        # self.plot4.set_axis_labels('Time (s)', 'Value')

        Stylize.button([self.load_button])
        Stylize.set_start_button_active(self.start_button, True)

    def set_start_button_active(self, isActive: bool):
        Stylize.set_start_button_active(self.start_button, isActive)

    def set_loaded_trial_text(self, text: str):
        self.loaded_trial_text.setText(text)

    def set_sequence_table(self, config: Config.Config):

        table = self.sequence_table

        while(table.rowCount() > 0.5):
            table.removeRow(table.rowCount() - 1)

        for i in range(len(config.sequence_time_step)):
            table.insertRow(table.rowCount())
            
            item = QtWidgets.QTableWidgetItem()
            item.setText('')
            table.setVerticalHeaderItem(table.rowCount()-1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(config.sequence_time_step[i]))
            table.setItem(i, 0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(config.sequence_power[i]))
            table.setItem(i, 1, item)
            
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(config.sequence_temperature[i]))
            table.setItem(i, 2, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(config.sequence_mass_flow[i]))
            table.setItem(i, 3, item)
            # self.sequence_table.item(i, 0).setText(str(config.sequence_time_step[i]))
            # self.sequence_table.item(i, 1).setText(str(config.sequence_power[i]))
            # self.sequence_table.item(i, 2).setText(str(config.sequence_temperature[i]))
            # self.sequence_table.item(i, 3).setText(str(config.sequence_mass_flow[i]))

class Setup:
    def __init__(self, pyqt5: Ui_MainWindow):
        self.daq_status_label = pyqt5.setup_daq_status_label
        self.controller_status_label = pyqt5.setup_controller_status_label

        self.daq_port_field = pyqt5.setup_daq_port_field
        self.controller_port_field = pyqt5.setup_controller_port_field

        self.auto_connect_button = pyqt5.setup_autoconnect_button
        self.manual_connect_button = pyqt5.setup_manualconnect_button

        self.setting_ui_frequency_field = pyqt5.setup_ui_frequency_field
        self.apply_settings_button = pyqt5.setup_apply_settings_button

        Stylize.button([self.auto_connect_button, self.manual_connect_button, self.apply_settings_button])
        Stylize.set_button_active(self.auto_connect_button, False)



class UpdateThread(QThread):
    update_signal = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.wait_time = 0.5
        self.thread_is_running = True

    def set_max_frequency(self, frequency):
        self.wait_time = 1 / frequency

    def run(self):
        while (self.thread_is_running):
            self.update_signal.emit()
            time.sleep(0.05)
        
        