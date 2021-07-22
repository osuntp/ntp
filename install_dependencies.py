import sys
import subprocess

# Run this script to install all dependencies required for the python code. Script taken from this link:
# https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/

# If this script doesn't work, here are the command lines so you can install packages manually:
# pip install pandas
# pip install pyserial
# pip install matplotlib

# implement pip as a subprocess:

# Data Analysis Library
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'pandas'])

# Access to Serial Port
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'pyserial'])

# Visualization and Plotting
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'matplotlib'])

