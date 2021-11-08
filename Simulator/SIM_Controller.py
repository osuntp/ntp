from Simulator import Controller
import time

if __name__ == "__main__":
    C = Controller(port='COM7',baudrate=9600)
    try:

        C.connect()
        C.connect_to_app(ID='Controller')
        while C.app_connected:
            C.receive_command()
            C.disconnect_from_app(ID='Controller')
            time.sleep(0.1)
    except KeyboardInterrupt:
        C.ser.close()
