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
        """This method initialzes the UIDriver object as well as all relevant member variables"""

        # init member variables
        self.width = 0
        self.height = 0
        self.window = None

        # inits pygame and gets the display size
        pygame.init()
        display_info = pygame.display.Info()

        # calculates the size of the window we want to initialize
        self.width = display_info.current_w * 0.8
        self.height = display_info.current_h * 0.8

        # initializes the window using the previously calculated sizes
        self.window = pygame.display.set_mode((self.width, self.height))

        # sets the title of the window
        pygame.display.set_caption("Battleship")
        log("UIDriver.__init__(self): Window initialized successfully")


    def draw(self, GS, do_transition):
        # draws the game state it is passed, should return True if successful
        #  will update which buttons are on depending on GS 
        pass

    def draw_main_menu(self):
        """Draws main menu and returns the user's selection
        @return dictionary: main menu settings in a dictionary"""
        self.window.fill((0, 0, 100)) # royal blue background
        pygame.display.flip()

        # log that we've drawn the main menu
        log("UIDriver.draw_main_menu(self): Main menu drawn successfully")

        # waits for user inputs and returns the selection
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


        return 



    def wait_for_shot(self):
        # waits for UI input and returns what square was clicked.
        # buttons being on/off is handled in draw()
        pass

    def run(self):
        """Main loop for running the UI"""
        # start with main menu
        self.draw_main_menu()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
