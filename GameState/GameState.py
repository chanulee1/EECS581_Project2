"""
GameState.py
Authors:
    - First Last
    - First Last
Date: 9/2/2024

Purpose: does the backend driving of the battle ship game state
"""
from Logger.Logger import *

class GameState:
    def __init__(self):
        log("GameState.__init__(self): I'm in GameState!")
        # pandas array for each player's board
        # which turn are we on
        pass

    def fire(self, coord):
        # returns a string "hit", "miss", "gameover"
        # updates game board (p1/p2's) accordingly
        pass

    def add_ship(self, start, end):
        # adds a ship between start and end
        # needs to check if the ship is a line
        pass
