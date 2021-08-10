
# Modified from: http://www.science.smith.edu/dftwiki/index.php/PySerial_Simulator

# fakeSerial.py
# D. Thiebaut
# A very crude simulator for PySerial assuming it
# is emulating an Arduino.

import time
import threading
import random
import serial


# a Serial class emulator 
class VirtualArduino:

    _data:str = ""
    in_waiting: int = 0

    # Random Numbers
    num_of_traces = 11
    traces = []

    starting_value = 25
    min_value = 0
    max_value = 50
    variation = 10

    def connect_to_serial(self, port):
        self.start_time = time.time()
        self.serial = serial.Serial(port)

        self.data_loop_thread = threading.Thread(target=self.data_loop)

        for i in range(self.num_of_traces - 1):
            self.traces.append(self.starting_value)

        self.traces.insert(0, self.time_passed_in_ms())

        self.data_loop_thread.start()


    def data_loop(self):

        self.loop_is_running = True
        
        self.serial.write('<id, da>\n'.encode('utf-8'))

        data_point_index = 0

        while(self.loop_is_running):

            new_data_line = "<da, "
            new_data_line += str(data_point_index)
            new_data_line += ", "
            new_data_line += str(self.time_passed_in_ms())

            for i in range(len(self.traces)):
                self.traces[i] = self.add_random_value(self.traces[i])

                new_data_line += ", "
                new_data_line += str(self.traces[i])

            new_data_line += ">\n"

            self.serial.write(new_data_line.encode('utf-8'))

            data_point_index += 1
            time.sleep(0.01)

    def disconnect_from_serial(self):
        self.loop_is_running = False

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