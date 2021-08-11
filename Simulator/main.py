from Simulator import DAQ

if __name__ == "__main__":
    D = DAQ(port='COM1',baudrate=9600)
    D.connect()
    D.write(b'test')

    