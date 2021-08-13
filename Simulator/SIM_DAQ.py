from Simulator import DAQ
import time

if __name__ == "__main__":
    D = DAQ(port='COM5',baudrate=9600)
    try:

        D.connect()
        D.connect_to_app(ID='DAQ')
        while D.app_connected:
            D.send_data()
            D.disconnect_from_app(ID='DAQ')
            time.sleep(1)
    except KeyboardInterrupt:
        D.ser.close()