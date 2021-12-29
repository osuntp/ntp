import sys
import glob

import random
import serial
from serial.serialutil import SerialException
from Model import Model
from Log import Log
import time

import threading
import LD
from enum import Enum
from SettingsManager import SettingsManager

class Arduino(Enum):
    DAQ = 1
    CONTROLLER = 2

class DeveloperArduinos:

    time_of_last_daq_message = 0
    time_between_daq_messages = 1

    @classmethod
    def new_daq_message_available(cls):
        
        current_time = time.time()

        message_available = (current_time - cls.time_of_last_daq_message) > cls.time_between_daq_messages

        if(message_available):
            cls.time_of_last_daq_message = current_time

        return message_available

    @classmethod
    def get_daq_message(cls, num_of_daq_values):

        message = '<stdout, '

        value = round(random.random(), 2)

        message += str(value)

        for i in range(num_of_daq_values-1):
            message += ', '

            value = round(random.random(), 2)       
            message += str(value)
        
        message += '>'
        
        return message

class SerialMonitor:
    daq_id = 'daq'
    controller_id = 'controller'
    daq_arduino = None
    tsc_arduino = None
    baudrate = 9600
    daq_buffer = ''
    tsc_buffer = ''
    is_fully_connected = False

    in_developer_mode = False

    model: Model = None

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def write(self, arduino: Arduino, message: str):

        if(self.in_developer_mode):
            print('Message to TSC: ' + message)
            return

        if(arduino == Arduino.CONTROLLER):
            self.tsc_arduino.write(message.encode('utf-8'))
        elif(arduino == Arduino.DAQ):
            self.daq_arduino.write(message.encode('utf-8'))

    def connect_arduinos(self, daq_port: str, tsc_port:str):
        
        if(self.in_developer_mode):
            return

        # CONNECT DAQ
        try:
            if(self.daq_arduino is None):
                self.daq_arduino = serial.Serial(port=daq_port, baudrate = self.baudrate, write_timeout = 0)
                
                waiting_for_response = True

                time_out = time.time() + 2

                while(waiting_for_response):

                    in_waiting = self.daq_arduino.in_waiting
                    
                    if(in_waiting > 0):
                        self.daq_buffer += self.daq_arduino.read(in_waiting).decode('utf-8')

                        while '\n' in self.daq_buffer: #split data line by line and store it in var
                            raw_message_line, self.daq_buffer = self.daq_buffer.split('\n', 1)
                            clean_message = LD.clean(raw_message_line)

                            if(clean_message[0] == 'DAQ'):
                                self.model.daq_status_text = 'Connected'
                                waiting_for_response = False
                                self.start_daq_monitor_loop()

                    if(time.time() > time_out):
                        self.model.daq_status_text = 'Connection Timed Out'
                        self.daq_arduino.close()
                        self.daq_arduino = None
                        waiting_for_response = False

                    time.sleep(0.1)
        except SerialException:
            self.model.daq_status_text = 'Invalid Port'

        # CONNECT CONTROLLER
        try:

            if(self.tsc_arduino is None):
                self.tsc_arduino = serial.Serial(port=tsc_port, baudrate = self.baudrate, write_timeout = 0)

                time_out = time.time() + 2
                waiting_for_response = True

                while(waiting_for_response):
                    in_waiting = self.tsc_arduino.in_waiting

                    if(in_waiting > 0):
                        self.tsc_buffer += self.tsc_arduino.read(in_waiting).decode('utf-8')

                        while '\n' in self.tsc_buffer:
                            raw_message_line, self.tsc_buffer = self.tsc_buffer.split('\n',1)
                            clean_message = LD.clean(raw_message_line)

                            if(clean_message[0] == 'TSC'):
                                self.model.tsc_status_text = 'Connected'
                                waiting_for_response = False
                                self.start_tsc_monitor_loop()
                    time.sleep(0.1)

                    if(time.time() > time_out):
                        self.model.tsc_status_text = 'Connection Timed Out'
                        self.tsc_arduino.close()
                        self.tsc_arduino = None
                        waiting_for_response = False
        except SerialException:
            self.model.tsc_status_text = 'Invalid Port'

        self.is_fully_connected = self.tsc_arduino is not None and self.daq_arduino is not None

        if(self.is_fully_connected):
            self.model.try_to_enable_start_button()
            SettingsManager.save_arduino_ports(daq_port, tsc_port)

    def start_daq_monitor_loop(self):
        self.data_collection_thread = threading.Thread(target = self.daq_monitor_loop)
        self.data_collection_thread.start()

    def daq_monitor_loop(self):

        self.daq_monitor_loop_is_running = True

        while(self.daq_monitor_loop_is_running):

            self.read_from_daq()

            time.sleep(0.01)

        print('data collection loop exiting')

    def start_tsc_monitor_loop(self):
        self.tsc_monitor_thread= threading.Thread(target = self.tsc_monitor_loop)
        self.tsc_monitor_thread.start()

    def tsc_monitor_loop(self):
        self.tsc_monitor_loop_is_running = True

        while(self.tsc_monitor_loop_is_running):

            self.read_from_tsc()

            time.sleep(0.01)

    def read_from_tsc(self):
        if(self.tsc_arduino is None):
            return

        in_waiting = self.tsc_arduino.in_waiting
        
        if(in_waiting > 0):
            # Add everything from serial to daq_buffer
            self.tsc_buffer += self.tsc_arduino.read(in_waiting).decode('utf-8')

            while '\n' in self.tsc_buffer: #split data line by line and store it in var
                raw_message_line, self.tsc_buffer = self.tsc_buffer.split('\n', 1)

                clean_message = LD.clean(raw_message_line)
                self.__handle_tsc_message(clean_message)

    def read_from_daq(self):

        if(self.in_developer_mode):
            
            if(DeveloperArduinos.new_daq_message_available()):

                # The number of values is LD.columns-3. Columns currently includes Time, Valve Position and Heater Status which are all appended by model.
                message = DeveloperArduinos.get_daq_message(len(LD.columns)-3)

                clean_message = LD.clean(message)
                self.__handle_daq_message(clean_message)
            
            return

        if(self.daq_arduino is None):
            return

        in_waiting = self.daq_arduino.in_waiting
        if(in_waiting > 0):

            # Add everything from serial to daq_buffer
            self.daq_buffer += self.daq_arduino.read(in_waiting).decode('utf-8')

            while '\n' in self.daq_buffer: #split data line by line and store it in var
                raw_message_line, self.daq_buffer = self.daq_buffer.split('\n', 1)

                clean_message = LD.clean(raw_message_line)
                self.__handle_daq_message(clean_message)

    def __handle_daq_message(self, message: list):
        prefix = message[0]

        message.pop(0)

        if(prefix == 'stdout'):
            self.model.update(message)
        elif(prefix == 'stdinfo'):
            Log.daq.info(message[0])
        elif(prefix == 'stderr'):
            Log.daq.error(message[0])
        elif(prefix == 'DAQ'):
            Log.daq.debug('Arduino Debug: Unexpected ID message from ' + prefix + '. Ignoring this message.')       
        else:
            Log.daq.warning('Unknown message type received from DAQ. The prefix was ' + prefix)    

    def __handle_tsc_message(self, message: list):
        prefix = message[0]

        message.pop(0)

        if(prefix == 'stdout'):
            Log.tsc.warning('Received stdout message from TSC')
        elif(prefix == 'stdinfo'):
            Log.tsc.info(message[0])
        elif(prefix == 'stderr'):
            Log.tsc.error(message[0])
        elif(prefix == 'TSC'):
            Log.tsc.debug('Arduino Debug: Unexpected ID message from ' + prefix + '. Ignoring this message.')        
        else:
            Log.tsc.warning('Unknown message type received from TSC. The prefix was ' + prefix)   

    def disconnect_arduinos(self):
        if(self.daq_arduino is not None):
            self.write(Arduino.DAQ, '<DAQ STOP>\n')
            waiting_for_response = True
            while(waiting_for_response):
                in_waiting = self.daq_arduino.in_waiting

                if(in_waiting > 0):
                    self.daq_buffer += self.daq_arduino.read(in_waiting).decode('utf-8')
                    
                    while '\n' in self.daq_buffer:
                        raw_message_line, self.daq_buffer = self.daq_buffer.split('\n',1)
                        clean_message = LD.clean(raw_message_line)
                        
                        if(clean_message[0] == 'DAQ'):
                            waiting_for_response = False
                            self.model.daq_is_connected = False
                time.sleep(0.01)

            self.daq_arduino.close()
            self.daq_arduino = None

        if(self.tsc_arduino is not None):
            self.write(Arduino.CONTROLLER, '<Controller STOP>\n')

            waiting_for_response = True
            while(waiting_for_response):
                in_waiting = self.tsc_arduino.in_waiting

                if(in_waiting > 0):
                    self.tsc_buffer += self.tsc_arduino.read(in_waiting).decode('utf-8')

                    while '\n' in self.tsc_buffer:
                        raw_message_line, self.tsc_buffer = self.tsc_buffer.split('\n',1)
                        clean_message = LD.clean(raw_message_line)
                        if(clean_message[0] == 'TSC'):
                            waiting_for_response = False
                            self.model.controller_is_connected = True

            self.tsc_arduino.close()
            self.tsc_arduino = None

        self.daq_monitor_loop_is_running = False
        self.tsc_monitor_loop_is_running = False

    def auto_connect_arduinos(self):
        ports = self.__get_serial_ports()

        for port in ports:
            print(str(port))
            connection = serial.Serial(port=port, baudrate=self.baudrate)

            timeout = time.time() + 5

            # Wait for arduino's ID signal or a time out
            while time.time() < timeout:

                time.sleep(0.1)
                    
                # If ID line has been sent from Arduino
                if (connection.in_waiting > 0):
                    message = connection.readline().decode('utf-8')

                    clean_message = LD.clean(message)
                    prefix = clean_message[0]

                    if(prefix == 'id'):

                        arduino_id = clean_message[1]

                        if(arduino_id == self.daq_id):
                            self.daq_arduino = connection

                        elif(arduino_id == self.controller_id):
                            self.controller_arduino = connection
                            
                        else:
                            Log.python.error('SerialMonitor: connect_arduinos(): arduino_id does not match either possible arduino ids')
                    else:
                        Log.python.error('SerialMonitor: connect_arduinos(): Expected ID prefix from arduino message. Instead received this prefix: ' + str(prefix))

                    break

    def on_window_exit(self):
        try:
            self.daq_monitor_loop_is_running = False
            self.data_collection_thread.join()
        except AttributeError:
            pass
        try:
            self.tsc_monitor_loop_is_running = False
            self.tsc_monitor_thread.join()
        except AttributeError:
            pass
        #self.disconnect_arduinos()



    def set_developer_mode(self, in_developer_mode):

        self.in_developer_mode = in_developer_mode     

        if(in_developer_mode):
            self.disconnect_arduinos()
            self.is_fully_connected = True

            self.model.daq_status_text = 'Developer Mode'
            self.model.tsc_status_text = 'Developer Mode'

            self.start_daq_monitor_loop()
            self.start_tsc_monitor_loop()
        else:
            self.disconnect_arduinos()
            self.is_fully_connected = False

            self.model.daq_status_text = 'Not Connected'
            self.model.tsc_status_text = 'Not Connected'
            
        self.model.try_to_enable_start_button()

# Modified From: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def __get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]

    # Not sure how glob works, assuming this wont be an issue since we're using windows. Will revisit if we want to release for other platforms.
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        Log.python.error('SerialMonitor: __get_serial_ports(): Tried to open ports on unsupported platform.')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result

if __name__ == "__main__":
    print(__get_serial_ports())