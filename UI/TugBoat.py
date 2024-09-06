"""
UIDriver.py
Authors:
    - Chase Horner
    - Katharine Swann
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

    def update(self, mouse_x, mouse_y): #NEED to rotate vertically, handle here or?
        window_width, window_height = self.surface.get_size() #get window size for reference

        rect_width = int(window_width * 0.2)   # 20% of the window's width
        rect_height = int(window_height * 0.1)  # 10% of the window's height

        go_x = int(window_width * 0.5) - rect_width // 2 #dimensions for go button from UIDriver.py
        go_y = int(window_height * 0.75) - rect_height // 2

        if self.dragging: #this is new code to attempt to keep boats within the window
            boat_x = mouse_x - self.rect.width // 2  #take half width and height to center baots
            boat_y = mouse_y - self.rect.height // 2 

            boat_x = max(0, min(boat_x, window_width - self.rect.width))  # lock locations 
            boat_y = max(0, min(boat_y, window_height - self.rect.height))

            boat_rect = pygame.Rect(boat_x, boat_y, self.rect.width, self.rect.height)
            go_button_rect = pygame.Rect(go_x, go_y, rect_width, rect_height)

            if boat_rect.colliderect(go_button_rect): # create a if statement for collide with preset GO button location based on window size
                if boat_x < go_x:
                    boat_x = go_x - self.rect.width # move left
                elif boat_x + self.rect.width > go_x + rect_width:
                    boat_x = go_x + rect_width  # move right

                if boat_y < go_y:
                    boat_y = go_y - self.rect.height  # move up
                elif boat_y + self.rect.height > go_y + rect_height:
                    boat_y = go_y + rect_height  # move down 

            self.rect.topleft = (boat_x, boat_y)