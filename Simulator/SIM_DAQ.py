from Simulator import DAQ
import time

if __name__ == "__main__":
    D = DAQ(port='COM1',baudrate=9600)
    D.connect()
    D.connect_to_app(ID='DAQ')
    while D.app_connected:
        D.send_data()
        D.disconnect_from_app(ID='DAQ')
        time.sleep(5)
