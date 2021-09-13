## import the serial library
import serial

## Boolean variable that will represent 
## whether or not the arduino is connected
connected = False

## establish connection to the serial port that your arduino 
## is connected to.

locations=['COM3']

for device in locations:
    try:
        print(f'Trying to connect on {device}')
        ser = serial.Serial(device, 9600)
        break
    except:
        print(f'Failed to connect on {device}')

## loop until the arduino tells us it is ready
while not connected:
    serin = ser.read()
    connected = True

## open text file to store the current 
##gps co-ordinates received from the rover    
text_file = open("C:\\Users\\noahr\\Documents\\GitHub\\ntp\\sandbox\\text.txt", 'w')
## read serial data from arduino and 
## write it to the text file 'position.txt'
try:
    while 1:
        if ser.inWaiting():
            x=ser.readline()
            print(x) 
            text_file.write(x.decode('utf-8'))
            if x=="\n":
                text_file.seek(0)
                text_file.truncate()
            text_file.flush()
except KeyboardInterrupt:
    ## close the serial connection and text file
    text_file.close()
    ser.close()