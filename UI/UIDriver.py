"""
UIDriver.py
Authors:
    - Pierce Lane
    - First Last
Date: 9/2/2024

Purpose: drives the UI of the battleship game
"""
from Logger.Logger import *

class UIDriver:
    def __init__(self):
        log("I'm in UIDriver!")
        # should create the window and draw the main menu
        pass

    def draw(self, GS, do_transition):
        # draws the game state it is passed, should return True if successful
        #  will update which buttons are on depending on GS 
        pass

    def draw_main_menu(self):
        # draws main menu, will be run on initialization
        pass

    def wait_for_shot(self):
        # waits for UI input and returns what square was clicked.
        #  buttons being on/off is handled in draw()
        pass

if __name__ == "__main__":
    print("Put debug code here")