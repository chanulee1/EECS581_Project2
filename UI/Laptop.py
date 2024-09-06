"""
Laptop.py
Authors:
    - Pierce Lane
Date: 9/6/2024

Purpose: holds the laptop (grid) objects and can do some functions on them
"""
import pygame 

class Tile:
    def __init__(self, top_left, bottom_right, hitstr):
        # store position
        self.top_left = top_left
        self.bottom_right = bottom_right
        # store what hit information we have ("hit", "miss", "unknown")
        self.hitstr = hitstr

class Laptop:
    def __init__(self, player_number, screen_wid, screen_height, tile_size = 90):
        """Constructor for laptop class

        @param player_number: int (1, 2) tracks player number
        @param screen_wid: int tracking screen width
        @param screen_height: int tracking screen height
        @param tile_size: int tracking grid tile pixel size"""

        # define class variables
        self.player_num = player_number
        self.SIZE_X = self.SIZE_Y = 10
        self.screen_wid = screen_wid
        self.screen_height = screen_height
        self.tile_size = tile_size

        # define our grid structure, a double array of tiles
        self.grid = None

        # generate the grid
        self.gen_grid()


    def gen_grid(self):
        """Generates the grid based on parameters given in constructor
        Can be regenerated as needed if any of those parameters change"""
        # redefine the grid
        self.grid = []
        # loop through it
        for row in range(self.SIZE_Y):
            # don't forget to add a row list
            self.grid.append([])
            # go through cols
            for col in range(self.SIZE_X):
                # do some math to find left and top pixel values
                ### NOTE: I'm not sure if this math is correct! ###
                left = (self.screen_wid/2) - (self.tile_size * 5) + col * self.tile_size
                top = (self.screen_height/2) + (self.screen_height/4) - (self.tile_size * 5) + row * self.tile_size
                
                # add tile size to get bottom, right values
                right = left + self.tile_size
                bottom = top + self.tile_size

                # concatonate those into a Tile object and store that
                self.grid[row].append(Tile((left, top), (right, bottom), "unknown"))