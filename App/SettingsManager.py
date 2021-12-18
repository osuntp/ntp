from configparser import ConfigParser
import configparser
from dataclasses import dataclass

@dataclass
class Settings:
    profile_index: str
    daq_port: str
    tsc_port: str


class SettingsManager:

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
    def open_settings_file(cls):
        # settings.set('main', 'profile_index', cls.profile_index)
        # settings.set('main', 'daq_port', cls.daq_port)
        # settings.set('main', 'tsc_port', cls.tsc_port)

        parser = ConfigParser()
        parser.read('Settings.ini')

        
        try:
            profile_index = parser.get('main', 'profile_name')
            daq_port = parser.get('main', 'daq_port')
            tsc_port = parser.get('main', 'tsc_port')

        except configparser.NoSectionError:
            profile_index = cls.profile_index
            daq_port = cls.daq_port
            tsc_port = cls.tsc_port

        
        settings = Settings(profile_index, daq_port, tsc_port)

        return settings


    @classmethod
    def save_arduino_ports(cls, daq_port, tsc_port):
        cls.daq_port = daq_port
        cls.tsc_port = tsc_port

        cls.create_settings_file()

    @classmethod
    def save_profile_index(cls, profile_index):
        cls.profile_index = profile_index

        cls.create_settings_file()