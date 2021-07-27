import logging
from UI.UI import UI

class Log:

    default_name = 'NTP_log'
    default_file_path = 'app.log'
    default_file_format = '%(asctime)s : %(process)d : %(levelname)s : %(message)s'

    ui_is_attached = False

    @classmethod
    def create(cls, name: str=None, file_path: str=None, file_format: str=None):

        if name is None:
            name = cls.default_name
        if file_path is None:
            file_path = cls.default_file_path
        if file_format is None:
            file_format = cls.default_file_format

        # Create separate logger from ROOT Logger
        cls.logger = logging.getLogger(name)
        cls.logger.setLevel(logging.DEBUG)
        
        # Specify custom handler
        handler = logging.FileHandler(file_path)
        handler.setLevel(logging.DEBUG)

        # Specify custom formatter
        formatter = logging.Formatter(file_format)

        handler.setFormatter(formatter)

        # cls.logger is now ready to be used
        cls.logger.addHandler(handler)

    @classmethod
    def attach_ui(cls, ui: UI):
        cls.ui = ui
        cls.ui_is_attached = True

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
        if(cls.ui_is_attached):
            cls.ui.logs.update_python_log()
        else:
            cls.logger.error('Log.py: __update_log_ui(): Tried to update the ui but it has not been assigned.')

    @classmethod
    def __handle_attribute_error(cls):
        cls.create()
        cls.error('Log.py: There was an AttributeError, the logger had not been created. Creating new Logger with default values.')
