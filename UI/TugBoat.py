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
        self.rect = pygame.Rect(x, y, 80*size, 80)
        self.color = (100, 100,100)
        self.dragging = False
        self.size = size
        self.surface = surface

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=10)

    def update(self, mouse_x, mouse_y):
        if self.dragging:
            #limits how low you can drag the boat
            y = min(525, mouse_y - self.rect.height // 2)
            self.rect.topleft = (mouse_x - self.rect.width // 2, y)

