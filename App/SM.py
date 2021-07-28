
import serial
from serial.serialutil import SerialException
import sys
import glob
from Log import Log
import time
import re

class SerialMonitor:

    daq_id = 'id_daq'
    controller_id = 'id_controller'
    arduinos_are_connected = False

    def __init__(self):
        self.baudrate = 9600
        self.DAQ_arduino = None
        self.controller_arduino = None

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def disconnect_arduinos(self):
        if not self.DAQ_arduino is None:
            self.DAQ_arduino.close()
            self.DAQ_arduino = None
        if not self.controller_arduino is None:
            self.controller_arduino.close()
            self.controller_arduino = None

    def connect_arduinos(self):
        ports = self.__get_serial_ports()
        for port in ports:
            connection = serial.Serial(port=port, baudrate=self.baudrate)

            timeout = time.time() + 5

            # Wait for arduino's ID signal or a time out
            while(True):

                time.sleep(0.1)

                # if Timeout
                if(time.time() > timeout):
                    Log.error('SerialMonitor: connect_arduinos(): Timed out while trying to connect to the arduino at port: ' + port)
                    return

                # If ID line has been sent from Arduino
                if (connection.in_waiting > 0):
                    break

            id = connection.readline().decode("utf-8")

            # Only letters and underscores - REPLACE WITH METHOD FROM LD.PY IN THE FUTURE
            id = re.sub(r'[\W]+', '', id)

            if(id == self.daq_id):
                self.DAQ_arduino = connection
                print('hit')

            elif(id == self.controller_id):
                self.controller_arduino = connection
            else:
                pass

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



    

if __name__ == "__main__":
    sm = SerialMonitor()
    sm.connect_arduinos()