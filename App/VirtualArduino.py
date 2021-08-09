
# Modified from: http://www.science.smith.edu/dftwiki/index.php/PySerial_Simulator

# fakeSerial.py
# D. Thiebaut
# A very crude simulator for PySerial assuming it
# is emulating an Arduino.

import time
import threading
import random


# a Serial class emulator 
class Serial:

    _data:str = ""
    in_waiting: int = 0

    # Random Numbers
    num_of_traces = 11
    traces = []

    starting_value = 25
    min_value = 0
    max_value = 50
    variation = 10

    ## init(): the constructor.  Many of the arguments have default values
    # and can be skipped when calling the constructor.
    def __init__( self, port='COM1', baudrate = 19200, timeout=1,
                  bytesize = 8, parity = 'N', stopbits = 1, xonxoff=0,
                  rtscts = 0):
        self.name     = port
        self.port     = port
        self.timeout  = timeout
        self.parity   = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff  = xonxoff
        self.rtscts   = rtscts
        self._isOpen  = True
        self._receivedData = ""

        self.start_time = time.time()

        for i in range(self.num_of_traces - 1):
            self.traces.append(self.starting_value)

        self.traces.insert(0, self.time_passed_in_ms())
        self.data_loop_thread = threading.Thread(target=self.data_loop)
        self.data_loop_thread.start()


    def data_loop(self):

        self.loop_is_running = True
        
        self.arduino_write('<id, da>\n')

        heater_value = 0

        while(self.loop_is_running):

            new_data_line = "<da, "
            new_data_line += str(self.time_passed_in_ms())

            for i in range(len(self.traces)):
                self.traces[i] = self.add_random_value(self.traces[i])

                new_data_line += ", "
                new_data_line += str(self.traces[i])

            new_data_line += ">\n"

            self._data += new_data_line

            self.in_waiting = len(self._data)
            time.sleep(1)

    def disconnect(self):
        self.loop_is_running = False

    ## isOpen()
    # returns True if the port to the Arduino is open.  False otherwise
    def isOpen( self ):
        return self._isOpen

    ## open()
    # opens the port
    def open( self ):
        self._isOpen = True

    ## close()
    # closes the port
    def close( self ):
        self._isOpen = False

    ## write()
    # writes a string of characters to the Arduino
    def write( self, string ):
        print( 'Arduino got: "' + string + '"' )
        self._receivedData += string

    ## read()
    # reads n characters from the fake Arduino. Actually n characters
    # are read from the string _data and returned to the caller.
    def read( self, n=1 ):

        
        s = self._data[0:n]
        self._data = self._data[n:]
        self.in_waiting = len(self._data)
        #print( "read: now self._data = ", self._data )
        return s

    ## readline()
    # reads characters from the fake Arduino until a \n is found.
    def readline( self ):

        returnIndex = self._data.index( "\n" )

        if returnIndex != -1:
            s = self._data[0:returnIndex+1]
            self._data = self._data[returnIndex+1:]
            self.in_waiting = len(self._data)

            return s
        else:
            return ""


    def arduino_write(self, message):
        self._data += message
        self.in_waiting = len(self._data)

    def time_passed_in_ms(self):
        return (time.time() - self.start_time)*1000

    def add_random_value(self, number: int):
        number += (random.randrange(0, 2 * self.variation) - self.variation)

        if(number > self.max_value):
            number = self.max_value
        elif(number < self.min_value):
            number = self.min_value

        return number

    ## __str__()
    # returns a string representation of the serial class
    def __str__( self ):
        return  "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % ( str(self.isOpen), self.port, self.baudrate ) \
               + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)"\
               % ( self.bytesize, self.parity, self.stopbits, self.xonxoff,
                   self.rtscts )