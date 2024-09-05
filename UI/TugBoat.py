"""
UIDriver.py
Authors:
    - Chase Horner
Date: 9/5/2024

Purpose: Creates a draggable boat object
"""
from Logger.Logger import *
import pygame

class TugBoat:
    def __init__(self, x, y, size, surface):
        #note: boats are able to be dragged off screen
        self.rect = pygame.Rect(x, y, 80*size, 80)
        self.color = (100, 100,100) #gray
        self.dragging = False #boolean determining if boat is being dragged or not
        self.size = size 
        self.surface = surface

    def draw(self): #method to draw tugboats
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=10)

    def update(self, mouse_x, mouse_y): #method for updating position
        window_width, window_height = self.surface.get_size() #get window size for ref.

        if self.dragging: #this is new code to attempt to keep boats within the window
            boat_x = mouse_x - self.rect.width // 2 #take half width and height to center baots
            boat_y = mouse_y - self.rect.height // 2 #for locating

            baot_x = max(0, min(boat_x, window_width - self.rect.width))
            boat_y = max(0, min(boat_y, window_height - self.rect.height))

            self.rect.topleft = (boat_x, boat_y)