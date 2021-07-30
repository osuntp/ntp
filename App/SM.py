
import serial
import sys
import glob

from Model import Model
from Log import Log
import time

import threading
import LD

class SerialMonitor:

    daq_id = 'daq'
    controller_id = 'controller'
    arduinos_are_connected = False

    def __init__(self, model: Model):
        self.baudrate = 9600
        self.model = model
        self.daq_arduino = None
        self.controller_arduino = None

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def write_to_controller(self, message):
        self.daq_arduino.write(message.encode())

    def disconnect_arduinos(self):
        if not self.daq_arduino is None:
            self.daq_arduino.close()
            self.daq_arduino = None

        if not self.controller_arduino is None:
            self.controller_arduino.close()
            self.controller_arduino = None

    def read_from_daq(self):
        if(self.daq_arduino.in_waiting > 0):
            raw_message_line = self.daq_arduino.readline().decode('utf-8')

            clean_message = LD.clean(raw_message_line)
 
            self.model.handle_daq_message(clean_message)
            
    def connect_arduinos(self):
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

loop_is_running = True

def read_loop():
    global monitor
    while(loop_is_running):     
        monitor.read_from_daq()

        time.sleep(1)

if __name__ == "__main__":
    model = Model()

    global monitor
    monitor = SerialMonitor(model)
    monitor.connect_arduinos()

    thread = threading.Thread(target = read_loop)
    thread.start()

    time.sleep(3)
    monitor.write_to_controller('test')
    time.sleep(3)
    monitor.write_to_controller('not test')
    time.sleep(3)

    loop_is_running = False

    monitor.disconnect_arduinos()
