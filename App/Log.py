import os
import datetime

class PythonLog:

    new_lines = ''

    name = 'APP'

    def info(self, message):
        message_type = 'INFO'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)
        
    def debug(self, message):
        message_type = 'DEBUG'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def warning(self, message):
        message_type = 'WARNING'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def error(self, message):
        message_type = 'ERROR'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)
        
class DAQLog:

    new_lines = ''

    name = 'DAQ'

    def info(self, message):
        message_type = 'INFO'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def debug(self, message):
        message_type = 'DEBUG'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def warning(self, message):
        message_type = 'WARNING'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def error(self, message):
        message_type = 'ERROR'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

class TSCLog:

    new_lines = ''

    name = 'TSC'

    def info(self, message):
        message_type = 'INFO'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def debug(self, message):
        message_type = 'DEBUG'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def warning(self, message):
        message_type = 'WARNING'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

    def error(self, message):
        message_type = 'ERROR'

        ui_line = Log.get_ui_line(message_type, message)
        file_line = Log.get_file_line(self.name, message_type, message)

        self.new_lines = self.new_lines + ui_line
        Log.add_to_file(file_line)

class Log:
    log_name = '.log'
    folder_name = 'Logs/'
    file_path = ''

    python: PythonLog = None

    @classmethod
    def create(cls):
        cls.python = PythonLog()
        cls.daq = DAQLog()
        cls.tsc = TSCLog()

        isdir = os.path.isdir(cls.folder_name)

        if (not isdir):
            os.mkdir(cls.folder_name)

        date = datetime.date.today()

        year = str(date.year)
        month = str(date.month)
        day = str(date.day)

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H%M%S")

        cls.file_path = cls.folder_name + year + '_' + month + '_' + day + '_' + current_time + cls.log_name

        with open(cls.file_path, 'a') as f:
            f.write('')

    @classmethod
    def add_to_file(cls, new_line):
        with open(cls.file_path, 'a') as f:
            f.write(new_line)

    @classmethod
    def get_ui_line(cls, message_type, message):
        now = datetime.datetime.now()
        time = now.strftime('%H:%M:%S.%f')

        ui_line = time + ' : ' + message_type + ' : ' + message + '\n'
        return ui_line

    @classmethod
    def get_file_line(cls, log_name, message_type, message):
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S.%f')

        file_line = log_name + ' : ' + date + ' : ' + time + ' : ' + message_type + ' : ' + message + '\n'
        return file_line

if __name__ == '__main__':
    Log.create()
    Log.python.info('test')

    print(Log.python.new_lines)
    Log.python.info('YAAA')

    print(Log.python.new_lines)