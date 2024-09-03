"""
main.py
Authors:
    - Pierce Lane
    - First Last
Date: 9/2/2024

Purpose: driver file for the battleship game
Inputs: N/A (-- could add command line args if we wanted to have a headless version)
"""

from UI.UIDriver import *
from GameState.GameState import *
from Logger.Logger import *

def main_menu_loop():
    # should wait for inputs from the main menu in UIDriver
    pass

def main():
    #clear_log()
    ui = UIDriver()
    gs = GameState()
    log("This is a test log!")

    # do main menu handling
    main_menu_loop()


    # main menu options: 
        # num ships
        # where ships go on p1 and p2 - GameState.add_ship(point1, point2)
    # once main menu options are inputted and stored, start main loop

    # main loop:
        # UIDriver.wait_for_shot()
        # GameState.fire()
            # check for game over here
        # UIDriver.draw() -- might need another function for drawing game over screen

    # play again feature?

    # close the window
    pass

if __name__ == "__main__":
    # parse command line args here if wanted
    main()