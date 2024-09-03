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
    # clear all logs
    clear_log()
    # create the UI object
    ui = UIDriver()
    # create the game state object
    gs = GameState()

    ## do main menu
    # draw the title Battleship
    ui.draw_title(True)
    # draw the ship number selector
    ui.draw_ship_nums(True, 3)
    # draw the ship box
    ui.draw_ship_box(True)

    # start with the number of ships each side gets
    num_ships = ui.get_num_ships()

    # undraw the title
    ui.draw_title(False)
    # undraw the ship number selector
    ui.draw_ship_nums(False)

    # draw player 1's laptop
    ui.draw_laptop(1)
    # get the placement of p1's ships
    p1ships = ui.get_ships(1)

    # draw player 2's laptop
        # this should account for the animation between them
    ui.draw_laptop(2)
    # get the placement of p2's ships
    p2ships = ui.get_ships(2)

    # finally, tell GameState what we've found out

    # then start the main loop
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