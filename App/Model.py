

class Model:
    def __init__(self):
        pass

    def handle_daq_message(self, message: list):

        prefix = message[0]

        if(prefix == 'da'):
            # add data point
            pass
        elif(prefix == 'er'):
            # arduino error
            pass
        elif(prefix == 'id'):
            # arduino id
            pass
        else:
            # unknown prefix, something went wrong with prefix
            pass