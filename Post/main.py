import logging
import os
import datetime

def init_logging():
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    LOG_DIR = f'{BASE_DIR}/logs/'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    today = datetime.datetime.now().strftime('%Y%m%d')
    i = 0
    while os.path.exists(f'{LOG_DIR}post_{today}_%s.log' % i):
        i += 1
    LOG_FILE = f'{LOG_DIR}post_{today}_%s.log' % i
    logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG,format='%(asctime)s : %(process)d : %(levelname)s : %(message)s')
    logging.info('Logging started')
    logging.info(f'Log file saved to {LOG_FILE}')


def main():
    init_logging()
    

if __name__ == "__main__":
    main()