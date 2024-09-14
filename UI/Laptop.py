"""
Laptop.py
Authors:
    - Pierce Lane
    - Chase Horner
    - Katharine Swann
Date: 9/6/2024

Purpose: holds the laptop (grid) objects and can do some functions on them
"""
import pygame 

class Tile:
    """Object for each spot on laptop grid, used to track location and clicking"""
    def __init__(self, top_left, bottom_right, clickable = False): # Store position
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.clickable = clickable

class Laptop: 
    SIZE_X = SIZE_Y = 10 # Grids for game play are 10 x 10
    
    def __init__(self, player_number, screen_wid, screen_height, tile_size = 90):
        """Constructor for laptop class

        @param player_number: int (1, 2) tracks player number
        @param screen_wid: int tracking screen width
        @param screen_height: int tracking screen height
        @param tile_size: int tracking grid tile pixel size"""

        # Define class variables
        self.player_num = player_number
        self.screen_wid = screen_wid
        self.screen_height = screen_height
        self.tile_size = tile_size

        # Define our grid structures, a double array of tiles
        self.their_grid = None
        self.our_grid = None

        # Generate the grid
        self.gen_grids()


    def gen_grids(self):
        """Generates the grids based on parameters given in constructor
        Can be regenerated as needed if any of those parameters change"""
        # Redefine the grid
        self.their_grid = []
        self.our_grid = []

        y_offset = self.screen_height * 0.1

        # Loop through it
        for row in range(Laptop.SIZE_Y):
            # Add a row list
            self.their_grid.append([])
            self.our_grid.append([])
            # Go through columns
            for col in range(Laptop.SIZE_X):
                # Find left and top pixel values
                left = (self.screen_wid/3) - (self.tile_size * 5) + col * self.tile_size
                top = (self.screen_height/3) - (self.tile_size * 5) + row * self.tile_size + y_offset
                
                # Add tile size to get bottom, right values
                right = left + self.tile_size
                bottom = top + self.tile_size

                # Concatonate those into a Tile object and store that
                self.our_grid[row].append(Tile((left, top), (right, bottom)))

                # Also store their grid, which is our grid translated right by the width of our grid + 50 pixels
                self.their_grid[row].append(Tile((left+self.tile_size*10+50, top), (right+self.tile_size*10+50, bottom), True))
