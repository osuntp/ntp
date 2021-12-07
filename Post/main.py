import logging
import os
import datetime
import pandas as pd
import seaborn as sns
import tkinter as tk
from tkinter import filedialog

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

def open_data_file():
    root = tk.Tk()
    root.withdraw()
    logging.info('Prompting user to select data file')
    return filedialog.askopenfilename()

def load_data_file(f):
    df = pd.read_table(f,index_col=0)
    logging.info('Converted data file to data frame')
    num_rows = len(df)
    logging.info(f'Dataframe has {num_rows} rows')
    return df

def main():
    init_logging()
    f = open_data_file()
    logging.info(f'Opened {f}')

    df = load_data_file(f)
    df.head()

if __name__ == "__main__":
    main()