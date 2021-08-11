import sys
import glob

import serial
from Model import Model
from Log import Log
import time

import threading
import LD
from enum import Enum

class Arduino(Enum):
    DAQ = 1
    CONTROLLER = 2

class SerialMonitor:
    daq_id = 'daq'
    controller_id = 'controller'
    arduinos_are_connected = False
    daq_arduino = None
    controller_arduino = None
    baudrate = 9600
    daq_buffer = ""

    model: Model = None

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def write(self, arduino: Arduino, message: str):
        if(arduino == Arduino.CONTROLLER):
            self.controller_arduino.write(message.encode())
        elif(arduino == Arduino.DAQ):
            self.daq_arduino.write(message.encode())

    def connect_arduinos(self, daq_port: str, controller_port:str):
        self.daq_arduino = serial.Serial(port=daq_port, baudrate = self.baudrate)
        # self.controller_arduino = serial.Serial(port=controller_port, baudrate = self.baudrate)


        waiting_for_ID_message = True
        while(waiting_for_ID_message):
            in_waiting = self.daq_arduino.in_waiting
            
            if(in_waiting > 0):
                self.daq_buffer += self.daq_arduino.read(in_waiting).decode('utf-8')
                while '\n' in self.daq_buffer: #split data line by line and store it in var
                    raw_message_line, self.daq_buffer = self.daq_buffer.split('\n', 1)
                    clean_message = LD.clean(raw_message_line)
                    if(clean_message[0] == "DAQ"):
                        self.daq_arduino.write('<DAQ START>\n'.encode('utf-8'))
                        self.daq_buffer = ''
                        waiting_for_ID_message = False

            time.sleep(0.01)
        self.start_data_collection_loop()

    def disconnect_arduinos(self):
        if self.daq_arduino is not None:
            self.daq_arduino.close()
            self.daq_arduino = None

        if self.controller_arduino is not None:
            self.controller_arduino.close()
            self.controller_arduino = None

    def read_from_daq(self):

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
        elif(prefix == 'stderr'):
            print('Arduino Error: ' + message[0])
        elif(prefix == 'DAQ'):
            print('Arduino Debug: Unexpected ID message from ' + prefix + '. Ignoring this message.')
        else:
            Log.warning('Unknown message type received from DAQ. The prefix was ' + prefix)    

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
                            Log.error('SerialMonitor: connect_arduinos(): arduino_id does not match either possible arduino ids')
                    else:
                        Log.error('SerialMonitor: connect_arduinos(): Expected ID prefix from arduino message. Instead received this prefix: ' + str(prefix))

                    break

        # TODO: Uncomment this when we're ready to work with two arduinos at once.
        # If one arduino wasn't able to connect, disconnect the other.
        # if self.DAQ_arduino is None:
        #     Log.error('SerialMonitor: connect_arduinos(): Unable to connect DAQ Arduino, closing any open Arduino connections.')
        #     self.disconnect_arduinos()

        # elif self.controller_arduino is None:
        #     Log.error('SerialMonitor: connect_arduinos(): Unable to connect Controller Arduino, closing any open Arduino connections.')
        #     self.disconnect_arduinos()
        # else:
        #     self.arduinos_are_connected = True

    def start_data_collection_loop(self):
        self.data_collection_thread = threading.Thread(target = self.data_collection_loop)
        self.data_collection_thread.start()

    def data_collection_loop(self):

        self.loop_is_running = True

        while(self.loop_is_running):

            self.read_from_daq()

            time.sleep(0.01)

        print('data collection loop exiting')

    def on_window_exit(self):
        self.loop_is_running = False
        self.disconnect_arduinos()

# Modified From: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    def __get_serial_ports(self):
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
            Log.error('SerialMonitor: __get_serial_ports(): Tried to open ports on unsupported platform.')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result