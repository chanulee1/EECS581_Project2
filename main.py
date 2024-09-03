"""
main.py
Authors:
    - First Last
    - First Last
Date:

Purpose:
Inputs:
Outputs:
"""
from UI.UIDriver import *
from GameState.GameState import *

def main():
    # make a UIDriver object
    # make a GameState object
    # do main menu handling


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