"""
UIDriver.py
Authors:
    - Chase Horner
    - Katharine Swann
    - Michael Stang
Date: 9/5/2024

Purpose: Creates a draggable boat object
"""
from Logger.Logger import *
import pygame

class TugBoat:
    tile_size = 40

    def __init__(self, x, y, size, surface):
        self.rect = pygame.Rect(x, y, self.tile_size*size, self.tile_size)
        self.color = (180, 180, 180)
        self.dragging = False 
        self.size = size 
        self.surface = surface
        self.is_horizontal = True
        self.original_pos = self.rect.topleft

    def draw(self): 
        #Method to draw tugboat
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=10)

    def update(self, mouse_x, mouse_y):
        #Calculate window size
        window_width, window_height = self.surface.get_size() 
        rect_width = int(window_width * 0.2) 
        rect_height = int(window_height * 0.1)

        #Dimensions for go button from UIDriver.py
        go_x = int(window_width * 0.5) - rect_width // 2 
        go_y = int(window_height * 0.75) - rect_height // 2

        #When dragging (event mousedown is on boat before event mouseup)
        if self.dragging: 
            # Take half width and height to center boats
            boat_x = mouse_x - self.rect.width // 2  
            boat_y = mouse_y - self.rect.height // 2 

            #Lock locations 
            boat_x = max(0, min(boat_x, window_width - self.rect.width))  
            boat_y = max(0, min(boat_y, window_height - self.rect.height))

            boat_rect = pygame.Rect(boat_x, boat_y, self.rect.width, self.rect.height)
            go_button_rect = pygame.Rect(go_x, go_y, rect_width, rect_height)

            # Create a if statement for collide with preset GO button location based on window size
            # to prevent collision with GO button when placing ships
            if boat_rect.colliderect(go_button_rect):
                if boat_x < go_x:
                    # Move left
                    boat_x = go_x - self.rect.width 
                elif boat_x + self.rect.width > go_x + rect_width:
                    # Move right
                    boat_x = go_x + rect_width  

                if boat_y < go_y:
                    # Move up
                    boat_y = go_y - self.rect.height  
                elif boat_y + self.rect.height > go_y + rect_height:
                    # Move down 
                    boat_y = go_y + rect_height  

            self.rect.topleft = (boat_x, boat_y)

    def force_move(self, x, y):
        self.rect.topleft = (x, y)
        
    def rotate(self): # Function to rotate the boat using 'r' key
        # Swaps the height and width of the boat
        if self.is_horizontal:
            self.is_horizontal = False
        else:
            self.is_horizontal = True
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
