"""
UIDriver.py
Authors:
    - Pierce Lane
    - Holden Vail
    - Katharine Swann
Date: 9/2/2024

Purpose: drives the UI of the battleship game
"""
from Logger.Logger import *
import pygame

class UIDriver:
    def __init__(self):
        log("I'm in UIDriver!")
        # should create the window and draw the main menu

        # gets the display size
        display_info = pygame.display.Info()

        # calculates the size of the window we want to initialize
        width = display_info.current_w * 0.8
        height = display_info.current_h * 0.8

        # initializes the window using the previously calculated sizes
        self.window = pygame.display.set_mode((width, height))

        # sets the title of the window
        pygame.display.set_caption("Battleship")
        
        # calls to draw the main menu
        self.draw_main_menu()

    def draw(self, GS, do_transition):
        # draws the game state it is passed, should return True if successful
        #  will update which buttons are on depending on GS 
        pass

    def draw_main_menu(self):
        # draws main menu, will be run on initialization
        pass

    def wait_for_shot(self):
        # waits for UI input and returns what square was clicked.
        # buttons being on/off is handled in draw()
        pass

if __name__ == "__main__":
    print("Put debug code here")
    # initialize pygame
    pygame.init()

    # create a UIDriver object
    ui_driver = UIDriver()

    # run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # quit pygame
    pygame.quit()