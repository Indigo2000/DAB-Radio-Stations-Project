# Program to import and display information about Antenna and Parameter data for DAB radio stations
import GUI
from GUI import *
import config


def main():
    # Launch the gui
    splash()


# Launch the splash screen and then the whole program
main()

# Upon exiting, write the current view to file
config.json_string = config.json_string[:len(config.json_string) - 2]
config.json_string = config.json_string + ',\n\"View":[\n{\"Current View\": ' + str(config.display_value) + '}\n]\n}'
json_handling.json_to_file('CurrentState.json', config.json_string)

