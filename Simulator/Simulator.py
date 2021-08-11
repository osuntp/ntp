import sys
import glob
import serial
from serial.serialutil import SerialException, Timeout


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

class DAQ:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = 1
        self.app_connected = False

    def connect(self):
        try:
            ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
            print('Connected to serial port.')
            self.ser = ser
            self.write(b'<DAQ START>\n')
            return ser
        except SerialException:
            print('Serial port already in use.')
        return None

    def wait_for_app(self):
        while not self.app_connected:
            message = self.readln()
            if message == '<DAQ START>\n':
                self.app_connected = True
        return True

    def send_data(self):
        pass

    def write(self, message):
        self.ser.write(message)
        print('Message sent')

    def readln(self):
        return self.ser.readline()
            
class Controller():
    pass