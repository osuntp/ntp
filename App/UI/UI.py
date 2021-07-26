
from numpy import vdot
from UI.QT5_Generated_UI import Ui_window
from UI.Stylize import Stylize

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
import logging as log

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

        Stylize.all_tabs(self.tabs, starting_tab = self.pyqt5.diagnostics_tab)
        Stylize.abort(self.abort_tab)

        self.diagnostics = Diagnostics(self.pyqt5)
        self.logs = Logs(self.pyqt5)

        # TEST SECTION: DELETE LATER
        self.TEST_diagnostics_button = self.pyqt5.TEST_diagnostics_page
        self.TEST_hot_stand_to_green_button = self.pyqt5.TEST_hot_stand_to_green
        self.TEST_hot_stand_to_red_button = self.pyqt5.TEST_hot_stand_to_red
        self.hot_stand_status_light = self.pyqt5.side_bar_hot_stand_status
        # END OF TEST SECTION

    def set_current_tab(self, tab_index):
        print(tab_index)
        log.debug('UI says tab changed')
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

    def update_logs(self):
        path = os.getcwd()
        path = path + "\\app.log"

        with open(path, 'r') as file:
            data_list = file.readlines()
            data = ""

            for line in data_list:
                data += line + "<br><br>"
            self.logs_python_log.setHtml(data)
            print(data)

class Diagnostics:
    def __init__(self, pyqt5:Ui_window):
        self.plot1 = Canvas(pyqt5.diagnostics_plot1, "Time (s)", "Temperature (C)")
        self.plot2 = Canvas(pyqt5.diagnostics_plot2, "Time (s)", "Pressure (Pa)")

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

    def read_log_file(self):
        path = os.getcwd()
        path = path + "\\app.log"

        with open(path, 'r') as file:
            data_list = file.readlines()
            data = ""

            for line in data_list:
                data += line + "<br><br>"
            self.python.setHtml(data)


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