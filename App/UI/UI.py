
from PyQt5.QtGui import QFont
from UI.QT5_Generated_UI import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
# from UI.QT5_Generated_UI import Ui_window
from UI.Stylize import Stylize

import pyqtgraph
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

class Logs:
    def __init__(self, pyqt5: Ui_MainWindow):
        self.python = pyqt5.logs_python_log

    def update_python_log(self, file_path: str):

        with open(file_path, 'r') as file:
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
        
        self.clear_all()
        self.add_row_to_blue_lines_table()

        Stylize.button(buttons)
        Stylize.table(self.blue_lines_table)
        Stylize.table(self.sequence_table)

    def add_row_to_blue_lines_table(self):
        table = self.blue_lines_table
        row_count = table.rowCount()

        table.insertRow(row_count)
        item = QtWidgets.QTableWidgetItem()
        item.setText('')
        table.setVerticalHeaderItem(table.rowCount(), item)

        combo_box_options = ['Mass Flow', 'Heater Current', 'Heater TC', 'Inlet TC', 'Midpoint TC', 'Outlet TC', 'Tank Press', 'Inlet Press', 'Midpoint Press', 'Outlet Press']
        combo = QtWidgets.QComboBox()

        for option in combo_box_options:
            combo.addItem(option)

        table.setCellWidget(row_count, 1, combo)


        combo_box_options = ['Min', 'Max']    
        combo = QtWidgets.QComboBox()

        for option in combo_box_options:
            combo.addItem(option)


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
        self.trial_name_field.setText('')
        self.description_field.setPlainText('')

    def clear_blue_line_table(self):
        table = self.blue_lines_table

        while(table.rowCount() > 0.5):
            
            table.removeRow(table.rowCount() - 1)

        # Result will be 1 empty row
        self.add_row_to_blue_lines_table()

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

        # Checkboxes - Plot1
        self.plot1_inlet_check = pyqt5.run_plot1_inlet_check
        self.plot1_midpoint_check = pyqt5.run_plot1_midpoint_check
        self.plot1_outlet_check = pyqt5.run_plot1_outlet_check
        self.plot1_heat_sink_check = pyqt5.run_plot1_heat_sink_check

        self.plot1_heat_sink_check.setChecked(True)

        # Checkboxes - Plot2
        self.plot2_inlet_check = pyqt5.run_plot2_inlet_check
        self.plot2_midpoint_check = pyqt5.run_plot2_midpoint_check
        self.plot2_outlet_check = pyqt5.run_plot2_outlet_check
        self.plot2_tank_check = pyqt5.run_plot2_tank_check

        self.plot2_tank_check.setChecked(True)

        # Checkboxes - Plot3
            # None

        # Checkboxes - Plot4
        self.plot4_valve_position_check = pyqt5.run_plot4_valve_position_check
        self.plot4_heater_duty_check = pyqt5.run_plot4_heater_duty_check
        self.plot4_openfoam_check = pyqt5.run_plot4_openfoam_check

        self.plot4_valve_position_check.setChecked(True)

        # Plot Settings
        line_width = 2
        margin_left = 10
        margin_top = 0
        margin_right = 130
        margin_bottom = 10
        background_color = (255,255,255)

        # Actual Plot - Plot1
        pyqt5.run_plot1.setXRange(-10, 0)
        pyqt5.run_plot1.setBackground(background_color)

        plot_item = pyqt5.run_plot1.getPlotItem()
        plot_item.layout.setContentsMargins(margin_left,margin_top,margin_right,margin_bottom)
        plot_item.setLabel('bottom', 'Time (s)')
        plot_item.setLabel('left', 'Temperature (C)')
        plot_item.showGrid(x=True, y=True)

        legend = plot_item.addLegend()
        legend.setParentItem(plot_item)
        legend.setOffset((-17,50))
        legend.setBrush(pyqtgraph.mkBrush(color=background_color))

        self.plot1_inlet = plot_item.plot(name = 'Inlet')
        self.plot1_midpoint = plot_item.plot(name = 'Midpoint')
        self.plot1_outlet = plot_item.plot(name = 'Outlet')
        self.plot1_heat_sink = plot_item.plot(name = 'Heat Sink')

        self.plot1_inlet.setPen(pyqtgraph.mkPen(color='b', width = line_width))
        self.plot1_midpoint.setPen(pyqtgraph.mkPen(color='r', width = line_width))
        self.plot1_outlet.setPen(pyqtgraph.mkPen(color='g', width = line_width))
        self.plot1_heat_sink.setPen(pyqtgraph.mkPen(color='c', width = line_width))


        # Actual Plot - Plot 2
        pyqt5.run_plot2.setXRange(-10, 0)
        pyqt5.run_plot2.setBackground(background_color)

        plot_item = pyqt5.run_plot2.getPlotItem()
        plot_item.layout.setContentsMargins(margin_left,margin_top,margin_right,margin_bottom)
        plot_item.setLabel('bottom', 'Time (s)')
        plot_item.setLabel('left', 'Pressure (Pa)')
        plot_item.showGrid(x=True, y=True)

        legend = plot_item.addLegend()
        legend.setParentItem(plot_item)
        legend.setOffset((-19,50))
        legend.setBrush(pyqtgraph.mkBrush(color=background_color))

        self.plot2_inlet = plot_item.plot(name = 'Inlet')
        self.plot2_midpoint = plot_item.plot(name = 'Midpoint')
        self.plot2_outlet = plot_item.plot(name = 'Outlet')
        self.plot2_tank = plot_item.plot(name = 'Tank')

        self.plot2_inlet.setPen(pyqtgraph.mkPen(color='b', width = line_width))
        self.plot2_midpoint.setPen(pyqtgraph.mkPen(color='r', width = line_width))
        self.plot2_outlet.setPen(pyqtgraph.mkPen(color='g', width = line_width))
        self.plot2_tank.setPen(pyqtgraph.mkPen(color='c', width = line_width))


        # Actual Plot - Plot 3
        pyqt5.run_plot3.setXRange(-10, 0)
        pyqt5.run_plot3.setBackground(background_color)

        plot_item = pyqt5.run_plot3.getPlotItem()
        plot_item.layout.setContentsMargins(margin_left,margin_top,margin_right,margin_bottom)
        plot_item.setLabel('bottom', 'Time (s)')
        plot_item.setLabel('left', 'Mass Flow (kg/s)')
        plot_item.showGrid(x=True, y=True)

        legend = plot_item.addLegend()
        legend.setParentItem(plot_item)
        legend.setOffset((-12,50))
        legend.setBrush(pyqtgraph.mkBrush(color=background_color))

        self.plot3_mass_flow = plot_item.plot(name = 'Mass Flow')

        self.plot3_mass_flow.setPen(pyqtgraph.mkPen(color='b', width = line_width))

        # Actual Plot - Plot 4
        pyqt5.run_plot4.setXRange(-10, 0)
        pyqt5.run_plot4.setBackground(background_color)

        plot_item = pyqt5.run_plot4.getPlotItem()
        plot_item.layout.setContentsMargins(margin_left,margin_top,margin_right,margin_bottom)
        plot_item.setLabel('bottom', 'Time (s)')
        plot_item.setLabel('left', 'Value')
        plot_item.showGrid(x=True, y=True)

        legend = plot_item.addLegend()
        legend.setParentItem(plot_item)
        legend.setOffset((0,50))
        legend.setBrush(pyqtgraph.mkBrush(color=background_color))

        self.plot4_valve_position = plot_item.plot(name = 'Valve Pos')
        self.plot4_heater_duty = plot_item.plot(name = 'Heater Duty')
        self.plot4_openFOAM = plot_item.plot(name = 'OpenFOAM')

        self.plot4_valve_position.setPen(pyqtgraph.mkPen(color='b', width = line_width))
        self.plot4_heater_duty.setPen(pyqtgraph.mkPen(color='r', width = line_width))
        self.plot4_openFOAM.setPen(pyqtgraph.mkPen(color='g', width = line_width))

        Stylize.button([self.load_button])
        Stylize.set_button_active(self.start_button, False)
        Stylize.set_pause_button_active(self.pause_button, False)
        Stylize.table(self.sequence_table)

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

    def set_sequence_table_row_bold(self, row_int):
        table = self.sequence_table

        bold_font = QFont()
        bold_font.setBold(True)

        normal_font = QFont()

        row_count = table.rowCount()
        column_count = table.columnCount()
        
        for i in range(row_count):
            for j in range(column_count):
                if(i == row_int):
                    table.item(i,j).setFont(bold_font)
                else:
                    table.item(i,j).setFont(normal_font)





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
        
        