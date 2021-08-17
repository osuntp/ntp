import sys
import glob
import serial
from serial.serialutil import SerialException
import random
import re

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

if __name__ == '__main__':
    print(serial_ports())

class Simulator:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = 1
        self.ser_connected = False
        self.ser = None
    
    def connect(self):
        ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
        print('Connected to serial port.')
        self.ser = ser
        self.ser_connected = True
        return ser
    
    def write(self, message):
        self.ser.write(message)
        print('Message sent')

    def readln(self):
        return self.ser.readline()

    def connect_to_app(self, ID):
        while not self.app_connected:
            if ID == 'DAQ':
                key = b'<DAQ START>\n'
                response = b'<DAQ>\n'
            else:
                key = b'<Controller START>\n'
                response = b'<Controller>\n'
            
            if(self.ser.in_waiting > 0):

                message = self.readln()
                print('line read')
                if message == key:
                    self.app_connected = True
                    self.write(response)
                    print('Connected to app.')
        return True

    def disconnect_from_app(self, ID):
        if self.app_connected:

            if(self.ser.in_waiting > 0):
                if ID == 'DAQ':
                    key = b'<DAQ STOP>\n'
                    response = b'<DAQ>\n'
                else:
                    key = b'<Controller STOP>\n'
                    response = b'<Controller>\n'
                message = self.readln()
                print(message)
                print(key)
                if message == key:
                    self.app_connected = False
                    self.write(response)
                    print('Stopped data')
                    return self.app_connected

class DAQ(Simulator):
    def __init__(self, port, baudrate=9600, timeout=1):
        self.app_connected = False
        Simulator.__init__(self, port, baudrate, timeout)

    def send_data(self):
        mass_flow = random.random()
        heater_current = random.random()
        heater_tc = random.random()
        heater_tc_it = random.random()
        inlet_tc = random.random()
        inlet_tc_it = random.random()
        midpoint_tc = random.random()
        midpoint_tc_it = random.random()
        outlet_tc = random.random()
        outlet_tc_it = random.random()
        tank_press = random.random()
        inlet_press = random.random()
        midpoint_press = random.random()
        outlet_press = random.random()
        message = f'<stdout, {mass_flow}, {heater_current}, {heater_tc}, {heater_tc_it}, {inlet_tc}, {inlet_tc_it}, {midpoint_tc}, {midpoint_tc_it}, {outlet_tc}, {outlet_tc_it}, {tank_press}, {inlet_press}, {midpoint_press}, {outlet_press}>\n'.encode('utf-8')
        self.write(message)
            
class Controller(Simulator):
    def __init__(self, port, baudrate=9600, timeout=1):
        self.app_connected = False
        Simulator.__init__(self, port, baudrate, timeout)

    def receive_command(self):
        if self.app_connected:
            if(self.ser.in_waiting > 0):
                message = self.readln().decode('utf-8')
                parts = re.findall('[<\s](.*?)[,>]',message)
                
                if(parts[0] == 'Controller STOP'):
                    self.app_connected = False
                    self.write(b'<Controller>\n')

                if len(parts) == 3:
                    if parts[0] == 'stdin':
                        if parts[1] == 'valve':
                            try:
                                float(parts[2])
                                self.write(f'<stdout, valve, {parts[2]}'.encode('utf-8'))
                            except ValueError:
                                self.write(f'<stderr, valve position not recognized: {parts[2]}'.encode('utf-8'))
                        elif parts[1] == 'heater':
                            if parts[2] == '1':
                                self.write(b'<stdout, heater, 1>\n')
                            elif parts[2] == '0':
                                self.write(b'<stdout, heater, 0>\n')
                            else:
                                self.write(f'<stderr, heater value not recognized: {parts[2]}'.encode('utf-8'))
                        else:
                            self.write(b'<stderr, command not recognized>\n')
                

                