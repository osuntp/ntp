from configparser import ConfigParser

class Settings:

    profile_index = 0

    daq_port = 'COM0'
    tsc_port = 'COM1'

    @classmethod
    def create_settings_file(cls):
        settings = ConfigParser()

        settings.add_section('main')

        settings.set('main', 'profile_index', cls.profile_index)
        settings.set('main', 'daq_port', cls.daq_port)
        settings.set('main', 'tsc_port', cls.tsc_port)

        file_name = 'Settings.ini'

        with open(file_name, 'w') as f:
            settings.write(f)
    
    @classmethod
    def save_arduino_ports(cls, daq_port, tsc_port):
        cls.daq_port = daq_port
        cls.tsc_port = tsc_port

        cls.create_settings_file()

    @classmethod
    def save_profile_index(cls, profile_index):
        cls.profile_index = profile_index