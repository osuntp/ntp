# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 04:57:18 2021

@author: Jacob Stonehill
"""
import serial

class Arduino:
    def __init__(self):
        self._serial_is_open = False

        # Default Value for port
        self.port = 'COM3'

    def set_COM(self, port: str):
        self.port = port

    def open_serial(self):
        self._serial_is_open = True
        
        self._serial = serial.Serial(port=self.port, baudrate=9600)
        
    def data_point_is_available(self):
        if not(self._serial_is_open):
            print('Warning: Arduino: data_point_is_available(): Tried to check for data point while serial is not open.')
            return False
        
        return self._serial.in_waiting > 0
    
    def get_data_point(self):
        if not(self._serial_is_open):
            print('Warning: Arduino: get_data_point(): Tried to get data point while serial is not open.')
            return 0
        
        return self._serial.readline().decode("utf-8").split(', ')
    
    def close_serial(self):
        self._serial_is_not_open = True
        self._serial.close()