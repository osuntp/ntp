from PyQt5 import QtWidgets
from typing import List
from PyQt5.QtGui import QFont
from Config import Config
from UI.QT5_Generated_UI import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
# from UI.QT5_Generated_UI import Ui_window
from UI.Stylize import Stylize
from SettingsManager import Settings

import pyqtgraph
from PyQt5 import QtWidgets
import time

class Window(QMainWindow):
    pass

class UI:
    app: QtWidgets.QApplication = None

    side_bar_hot_stand_is_lit = False
    side_bar_heater_is_lit = False
    side_bar_valve_open_is_lit = False

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

        self.sidebar_daqstatus = self.pyqt5.sidebar_daq_status
        self.sidebar_tscstatus = self.pyqt5.sidebar_tsc_status

        self.side_bar_hot_stand_status = self.pyqt5.side_bar_hot_stand_status
        self.side_bar_state_text = self.pyqt5.side_bar_state_status

        self.sidebar_massflow = self.pyqt5.sidebar_mass_flow
        self.sidebar_valveposition = self.pyqt5.sidebar_valve_position

        self.sidebar_heaterpower = self.pyqt5.sidebar_heater_power
        self.sidebar_heaterstatus = self.pyqt5.sidebar_heater_status
        self.sidebar_heatercurrent = self.pyqt5.sidebar_heater_current
        self.sidebar_heatertemp = self.pyqt5.sidebar_heater_temp

        self.sidebar_supplytemp = self.pyqt5.sidebar_supply_temp
        self.sidebar_inlettemp = self.pyqt5.sidebar_inlet_temp
        self.sidebar_midtemp = self.pyqt5.sidebar_midpoint_temp
        self.sidebar_outlettemp = self.pyqt5.sidebar_outlet_temp
        
        self.sidebar_supplypress = self.pyqt5.sidebar_supply_press
        self.sidebar_inletpress = self.pyqt5.sidebar_inlet_press
        self.sidebar_midpress = self.pyqt5.sidebar_midpoint_press
        self.sidebar_outletpress = self.pyqt5.sidebar_outlet_press

        self.sidebar_other_name = [self.pyqt5.sidebar_other1_name, self.pyqt5.sidebar_other2_name, self.pyqt5.sidebar_other3_name, self.pyqt5.sidebar_other4_name, self.pyqt5.sidebar_other5_name]
        self.sidebar_other = [self.pyqt5.sidebar_other1, self.pyqt5.sidebar_other2, self.pyqt5.sidebar_other3, self.pyqt5.sidebar_other4, self.pyqt5.sidebar_other5]

        self.setup = Setup(self.pyqt5)
        self.diagnostics = Diagnostics(self.pyqt5)
        self.logs = Logs(self.pyqt5)
        self.manual = Manual(self.pyqt5)
        self.configuration = Configuration(self.pyqt5)
        self.run = Run(self.pyqt5)

    def set_current_tab(self, tab_index):
        new_tab = self.tabs[tab_index]
        prev_tab = self.current_tab

        Stylize.set_current_tab(new_tab, prev_tab)

        self.tabs_widget.setCurrentIndex(tab_index)

        self.current_tab = new_tab

    def set_side_bar_state_text(self, text):
        self.side_bar_state_text.setText(text)

    def set_hot_stand_status_light_is_lit(self, isLit: bool):
        self.side_bar_hot_stand_is_lit = isLit
        Stylize.set_status_light_is_lit(self.side_bar_hot_stand_status, isLit)

    def set_abort_tab_clickable(self, is_active):
        self.abort_tab.setEnabled(is_active)

class Diagnostics:
    def __init__(self, pyqt5:Ui_MainWindow):

        self.plot1_inlet_check = pyqt5.diagnostics_plot1_inlet_field
        self.plot1_midpoint_check = pyqt5.diagnostics_plot1_midpoint_field
        self.plot1_outlet_check = pyqt5.diagnostics_plot1_outlet_field
        self.plot1_heater_check = pyqt5.diagnostics_plot1_heater_field

        self.plot2_inlet_check = pyqt5.diagnostics_plot2_inlet_field
        self.plot2_midpoint_check = pyqt5.diagnostics_plot2_midpoint_field
        self.plot2_outlet_check = pyqt5.diagnostics_plot2_outlet_field
        self.plot2_supply_check = pyqt5.diagnostics_plot2_supply_field

        self.plot1_inlet_check.setChecked(True)
        self.plot1_midpoint_check.setChecked(True)
        self.plot1_outlet_check.setChecked(True)
        self.plot1_heater_check.setChecked(True)

        self.plot2_inlet_check.setChecked(True)
        self.plot2_midpoint_check.setChecked(True)
        self.plot2_outlet_check.setChecked(True)
        self.plot2_supply_check.setChecked(True)

        self.plot1 = pyqt5.diagnostics_plot1.getPlotItem()
        self.plot2 = pyqt5.diagnostics_plot2.getPlotItem()

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

        # Plot Settings
        line_width = 2
        margin_left = 10
        margin_top = 0
        margin_right = 130
        margin_bottom = 10
        background_color = (255,255,255)

        # Actual Plot - Plot1
        self.plot1 = pyqt5.diagnostics_plot1
        pyqt5.diagnostics_plot1.setXRange(-10, 0)
        pyqt5.diagnostics_plot1.setBackground(background_color)

        plot_item = pyqt5.diagnostics_plot1.getPlotItem()
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
        self.plot1_heater = plot_item.plot(name = 'Heat Sink')

        self.plot1_inlet.setPen(pyqtgraph.mkPen(color='b', width = line_width))
        self.plot1_midpoint.setPen(pyqtgraph.mkPen(color='r', width = line_width))
        self.plot1_outlet.setPen(pyqtgraph.mkPen(color='g', width = line_width))
        self.plot1_heater.setPen(pyqtgraph.mkPen(color='c', width = line_width))

        # Actual Plot - Plot2
        self.plot2 = pyqt5.diagnostics_plot2
        pyqt5.diagnostics_plot2.setXRange(-10, 0)
        pyqt5.diagnostics_plot2.setBackground(background_color)

        plot_item = pyqt5.diagnostics_plot2.getPlotItem()
        plot_item.layout.setContentsMargins(margin_left,margin_top,margin_right,margin_bottom)
        plot_item.setLabel('bottom', 'Time (s)')
        plot_item.setLabel('left', 'Pressure (Pa)')
        plot_item.showGrid(x=True, y=True)

        legend = plot_item.addLegend()
        legend.setParentItem(plot_item)
        legend.setOffset((-17,50))
        legend.setBrush(pyqtgraph.mkBrush(color=background_color))

        self.plot2_inlet = plot_item.plot(name = 'Inlet')
        self.plot2_midpoint = plot_item.plot(name = 'Midpoint')
        self.plot2_outlet = plot_item.plot(name = 'Outlet')
        self.plot2_supply = plot_item.plot(name = 'Supply')

        self.plot2_inlet.setPen(pyqtgraph.mkPen(color='b', width = line_width))
        self.plot2_midpoint.setPen(pyqtgraph.mkPen(color='r', width = line_width))
        self.plot2_outlet.setPen(pyqtgraph.mkPen(color='g', width = line_width))
        self.plot2_supply.setPen(pyqtgraph.mkPen(color='c', width = line_width))

class Setup:
    def __init__(self, pyqt5: Ui_MainWindow):
        self.daq_status_label = pyqt5.setup_daq_status_label
        self.controller_status_label = pyqt5.setup_controller_status_label

        self.test_stand_behaviour_field = pyqt5.setup_teststand_behaviour_field

        self.developer_mode_field = pyqt5.setup_developer_mode_field

    def set_initial_values_from_settings(self, selected_behaviour_field: int, in_developer_mode: bool):
        self.test_stand_behaviour_field.setCurrentIndex(selected_behaviour_field)
        self.developer_mode_field.setChecked(in_developer_mode)

class Logs:
    def __init__(self, pyqt5: Ui_MainWindow):
        self.python = pyqt5.logs_python_log
        self.daq = pyqt5.logs_daq_log
        self.tsc = pyqt5.logs_controller_log

class Manual:
    def __init__(self, pyqt5: Ui_MainWindow):
        self.current_valve_position_label = pyqt5.manual_currentValvePosLabel
        self.send_valve_command_button = pyqt5.manual_sendValveCommandButton
        self.valve_field = pyqt5.manual_valveSpinBox

        self.current_heater_label = pyqt5.manual_currentHeaterLabel
        self.send_heater_command_button = pyqt5.manual_sendHeaterCommandButton
        self.heater_field = pyqt5.manual_heatersSpinBox

    def set_command_buttons_active(self, is_active):
        self.send_valve_command_button.setEnabled(is_active)
        self.send_heater_command_button.setEnabled(is_active)

class Configuration:
    def __init__(self, pyqt5: Ui_MainWindow):
        self.trial_name_field = pyqt5.configuration_trialname_field
        self.description_field = pyqt5.configuration_description_field
        self.trial_end_timestep_field = pyqt5.configuration_trial_end_timestep_field

        self.blue_lines_table = pyqt5.configuration_blue_lines_table
        self.blue_lines_plus_button = pyqt5.configuration_blue_lines_plus
        self.blue_lines_minus_button = pyqt5.configuration_blue_lines_minus

        self.sequence_table = pyqt5.configuration_sequence_table
        self.sequence_plus_button = pyqt5.configuration_sequence_plus
        self.sequence_minus_button = pyqt5.configuration_sequence_minus

        self.clear_button = pyqt5.configuration_clear_button
        self.load_button = pyqt5.configuration_load_button
        self.save_button = pyqt5.configuration_save_button
        self.send_to_run_page_button = pyqt5.config_send_to_run_page_button

        buttons = [self.save_button, self.load_button, self.clear_button, self.blue_lines_plus_button, self.blue_lines_minus_button, self.sequence_plus_button, self.sequence_minus_button, self.send_to_run_page_button]
        
        self.clear_all()

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

        combo_box_options = ['Mass Flow', 'Heater Current', 'Heater Temp', 'Inlet Temp', 'Midpoint Temp', 'Outlet Temp', 'Supply Press', 'Inlet Press', 'Midpoint Press', 'Outlet Press']
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

    def set_sequence_table_columns(self, column_names):
        table = self.sequence_table
        
        column_count = len(column_names)

        table.setColumnCount(column_count)

        for i in range(column_count):
            item = QtWidgets.QTableWidgetItem()
            item.setText(column_names[i])
            table.setHorizontalHeaderItem(i, item)

    def add_row_to_sequence_table(self):
        table = self.sequence_table
        row_count = table.rowCount()

        table.insertRow(row_count)

    def remove_row_from_sequence_table(self):
        table = self.sequence_table
        row_count = table.rowCount()

        if(row_count - 1 < 0.5):
            return

        table.removeRow(row_count - 1)

    def load_values(self, config:Config):
        self.clear_all()

        self.trial_name_field.setText(config.trial_name)
        self.description_field.setPlainText(config.description)

        blue_lines_row_count = len(config.blue_lines_time_step)

        table = self.blue_lines_table

        table.removeRow(0)

        for i in range(blue_lines_row_count):
            table.insertRow(table.rowCount())

            text = str(config.blue_lines_time_step[i])
            item = QtWidgets.QTableWidgetItem()
            item.setText(text)
            table.setItem(table.rowCount()-1, 0, item)

            combo_box_options = ['Mass Flow', 'Heater Current', 'Heater Temp', 'Inlet Temp', 'Midpoint Temp', 'Outlet Temp', 'Supply Press', 'Inlet Press', 'Midpoint Press', 'Outlet Press']
            combo = QtWidgets.QComboBox()

            for option in combo_box_options:
                combo.addItem(option)
            combo.setCurrentIndex(combo_box_options.index(config.blue_lines_sensor_type[i]))
            table.setCellWidget(table.rowCount()-1, 1, combo)

            combo_box_options = ['Min', 'Max']            
            combo = QtWidgets.QComboBox()

            for option in combo_box_options:
                combo.addItem(option)
            combo.setCurrentIndex(combo_box_options.index(config.blue_lines_limit_type[i]))
            table.setCellWidget(table.rowCount()-1, 2, combo)

            text = str(config.blue_lines_value[i])
            item = QtWidgets.QTableWidgetItem()
            item.setText(text)
            table.setItem(table.rowCount()-1, 3, item)

        sequence_row_count = len(config.sequence_values[0])

        table = self.sequence_table
        table.removeRow(0)

        for i in range(sequence_row_count):
            
            table.insertRow(table.rowCount())

            for j in range(len(config.sequence_values)):
                text = str(config.sequence_values[j][i])
                item = QtWidgets.QTableWidgetItem()
                item.setText(text)
                table.setItem(table.rowCount()-1, j, item)

        self.trial_end_timestep_field.setText(str(config.trial_end_timestep))

    def clear_all(self):
        self.clear_blue_line_table()
        self.clear_sequence_table()

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
    sequence_table_bold_row = -1

    def __init__(self, pyqt5: Ui_MainWindow):
        self.load_button = pyqt5.run_load_configuration_button
        self.start_button = pyqt5.run_start_button
        self.pause_button = pyqt5.run_pause_button
        self.loaded_trial_text = pyqt5.run_trialname
        self.sequence_table = pyqt5.run_test_sequence_table
        self.sequence_table_label = pyqt5.run_test_sequence_label

        self.plot1_apply_buffer_button = pyqt5.run_plot1_apply_buffer_button
        self.plot2_apply_buffer_button = pyqt5.run_plot2_apply_buffer_button
        self.plot3_apply_buffer_button = pyqt5.run_plot3_apply_buffer_button
        self.plot4_apply_buffer_button = pyqt5.run_plot4_apply_buffer_button

        self.plot1_buffer_field = pyqt5.run_plot1_buffer_field
        self.plot2_buffer_field = pyqt5.run_plot2_buffer_field
        self.plot3_buffer_field = pyqt5.run_plot3_buffer_field
        self.plot4_buffer_field = pyqt5.run_plot4_buffer_field

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
        self.plot1 = pyqt5.run_plot1
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
        self.plot2 = pyqt5.run_plot2
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
        self.plot3 = pyqt5.run_plot3
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
        self.plot4 = pyqt5.run_plot4
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
        Stylize.start_button(self.start_button)
        Stylize.end_button(self.pause_button)
        Stylize.table(self.sequence_table)

    def set_loaded_trial_text(self, text: str):
        self.loaded_trial_text.setText(text)

    def set_sequence_table_columns(self, column_names):
        table = self.sequence_table
        
        column_count = len(column_names)

        table.setColumnCount(column_count)

        for i in range(column_count):
            item = QtWidgets.QTableWidgetItem()
            item.setText(column_names[i])
            table.setHorizontalHeaderItem(i, item)

    def set_sequence_table(self, sequence_values: List, end_time: float):
        table = self.sequence_table

        while(table.rowCount() > 0.5):
            table.removeRow(table.rowCount() - 1)

        for i in range(len(sequence_values[0])):
            table.insertRow(table.rowCount())

            item = QtWidgets.QTableWidgetItem()
            item.setText('')
            table.setVerticalHeaderItem(table.rowCount()-1, item)

            for j in range(len(sequence_values)):

                item = QtWidgets.QTableWidgetItem()
                item.setText(str(sequence_values[j][i]))
                table.setItem(table.rowCount()-1, j, item)
        
        table.insertRow(table.rowCount())

        for j in range(len(sequence_values)):
            item  = QtWidgets.QTableWidgetItem()

            if(j == 0):
                item.setText('End Trial at ' + str(end_time) + 's')
            else:
                item.setText('')

            table.setItem(table.rowCount()-1, j, item)
        
    def set_sequence_table_row_bold(self, row_int):

        table = self.sequence_table

        bold_font = QFont()
        bold_font.setBold(True)

        normal_font = QFont()

        row_count = table.rowCount()
        column_count = table.columnCount()

        self.sequence_table_bold_row = row_int

        if(row_int == -1):
            row_int = row_count-1

        # print(row_count)
        for i in range(row_count):
            for j in range(column_count-1):
                
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