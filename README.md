# ntp
The repository for the Nuclear Thermal Propulsion experiments software.

## File Structure
### Arduino
*Contains the code used on the two Arduinos.*
1. daq.ino - Arduino code which collects data from the test stand and 
2. controller.ino - 
### App
1. main.py - 
2. OFI.py - openFOAM interface
3. Data.py - 

## Software Requirements
### OFI.py
Requirements:
- given boundary conditions as an argument, parse and write BC's into openFOAM case
- run openFOAM case
- measure and report openFOAM solver progress
- when openFOAM completes, report solution and especially required mass flow

Desirements:
- ability to fully configure changeDict and controlDict files
- ability to interrupt solver

### Data.py
Requirements:
- save data from Arduinos to csv files

Desirements:
- 