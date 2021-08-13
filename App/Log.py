import logging
from UI.UI import UI
import os

class Log:
    ui: UI = None
    file_path = None

    @classmethod
    def create(cls, log_name: str='NTP_log', file_name: str='app.log', file_format: str='%(asctime)s : %(process)d : %(levelname)s : %(message)s'):

        folder_name = 'Logs/'

        isdir = os.path.isdir(folder_name)

        if not (isdir):
            os.mkdir('Logs/')

        
        cls.file_path = folder_name + file_name

        # Create separate logger from ROOT Logger
        cls.logger = logging.getLogger(log_name)
        cls.logger.setLevel(logging.DEBUG)
        
        # Specify custom handler
        handler = logging.FileHandler(cls.file_path)
        handler.setLevel(logging.DEBUG)

        # Specify custom formatter
        formatter = logging.Formatter(file_format)

        handler.setFormatter(formatter)

        # cls.logger is now ready to be used
        cls.logger.addHandler(handler)

    @classmethod
    def info(cls, message: str):
        try:
            cls.logger.info(message)
        except AttributeError:
            cls.__handle_attribute_error()
            cls.logger.info(message)

        cls.__update_log_ui()

    @classmethod
    def debug(cls, message: str):
        try:
            cls.logger.debug(message)
        except AttributeError:
            cls.__handle_attribute_error()
            cls.logger.debug(message)

        cls.__update_log_ui()

    @classmethod
    def warning(cls, message: str):
        try:
            cls.logger.warning(message)
        except AttributeError:
            cls.__handle_attribute_error()
            cls.logger.warning(message)

        cls.__update_log_ui()

    @classmethod
    def error(cls, message: str):
        try:
            cls.logger.error(message)
        except AttributeError:
            cls.__handle_attribute_error()
            cls.logger.error(message)

        cls.__update_log_ui()

    @classmethod
    def __update_log_ui(cls):
        if(cls.ui is None):
            return

        cls.ui.logs.update_python_log(cls.file_path)
    @classmethod
    def __handle_attribute_error(cls):
        cls.create()
        cls.error('Log.py: There was an AttributeError, the logger had not been created. Creating new Logger with default values.')
