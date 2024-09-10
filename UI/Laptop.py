"""
Laptop.py
Authors:
    - Pierce Lane
Date: 9/6/2024

Purpose: holds the laptop (grid) objects and can do some functions on them
"""
import pygame 

class Tile:
    def __init__(self, top_left, bottom_right, clickable = False):
        # store position
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.clickable = clickable

class Laptop:
    SIZE_X = SIZE_Y = 10
    
    def __init__(self, player_number, screen_wid, screen_height, tile_size = 90):
        """Constructor for laptop class

        @param player_number: int (1, 2) tracks player number
        @param screen_wid: int tracking screen width
        @param screen_height: int tracking screen height
        @param tile_size: int tracking grid tile pixel size"""

        # define class variables
        self.player_num = player_number

        self.screen_wid = screen_wid
        self.screen_height = screen_height
        self.tile_size = tile_size

        # define our grid structures, a double array of tiles
        self.their_grid = None
        self.our_grid = None

        # generate the grid
        self.gen_grids()


    def gen_grids(self):
        """Generates the grids based on parameters given in constructor
        Can be regenerated as needed if any of those parameters change"""
        # redefine the grid
        self.their_grid = []
        self.our_grid = []
        # loop through it
        for row in range(Laptop.SIZE_Y):
            # don't forget to add a row list
            self.their_grid.append([])
            self.our_grid.append([])
            # go through cols
            for col in range(Laptop.SIZE_X):
                # do some math to find left and top pixel values
                ### NOTE: I'm not sure if this math is correct! ###
                left = (self.screen_wid/3) - (self.tile_size * 5) + col * self.tile_size
                top = (self.screen_height/3) - (self.tile_size * 5) + row * self.tile_size
                
                # add tile size to get bottom, right values
                right = left + self.tile_size
                bottom = top + self.tile_size

                # concatonate those into a Tile object and store that
                self.our_grid[row].append(Tile((left, top), (right, bottom)))

                # also store their grid, which is our grid translated right by
                # the width of our grid + 50 pixels
                self.their_grid[row].append(Tile((left+self.tile_size*10+50, top), (right+self.tile_size*10+50, bottom), True))
