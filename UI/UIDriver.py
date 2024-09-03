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
# temp import
from time import sleep

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

        # define and set background color
        self.bgcolor = (0, 161, 224)
        self.window.fill(self.bgcolor) # royal blue background

        # sets the title of the window
        pygame.display.set_caption("Battleship")
        pygame.display.flip()
        log("UIDriver.__init__(self): Window initialized successfully")

        # define uninitialized class variables
        self.p1_laptop = None   # p1 laptop object, should be another file
        self.p2_laptop = None   # p2 laptop object, should be another file
        self.cur_laptop = None  # current laptop being displayed
        self.go_button = None   # go button object
        self.ship_count = 3     # number of ships locked in via main menu

    def draw(self, GS, do_transition):
        # draws the game state it is passed, should return True if successful
        #  will update which buttons are on depending on GS 
        pass

    def wait_for_shot(self):
        # waits for UI input and returns what square was clicked.
        # buttons being on/off is handled in draw()
        pass
    
    def draw_go(self, do_delete=False):
        """Draws the GO button
        @param do_delete=False: boolean, if True will remove the element"""
        pass

    def wait_for_go(self):
        """Waits by spinning until the the GO button is pressed"""
        sleep(2)

    def draw_title(self, do_delete=False):
        """Draws the title text
        @param do_delete=False: boolean, if True will remove the element"""
        # first set font
        font = pygame.font.SysFont("Comic Sans MS", 300)
        # create a surface to render
        text_surface = font.render("Battleship", False, (255, 255, 255))
        # set the destination of the surface
        text_rect = text_surface.get_rect(center=(self.width/2, 200))

        # draw title text if not do_delete        
        if not do_delete:
            # draw it
            self.window.blit(text_surface, text_rect)
            
        # need to delete title text
        else:
            # draw a background-colored rectangle on it
            pygame.draw.rect(self.window, self.bgcolor, text_rect)
        
        # Update the display to reflect the changes
        pygame.display.update()

    def draw_ship_nums(self, do_delete=False):
        """Draws the ship number edit control
        @param do_delete=False: boolean, if True will remove the element"""
        pass

    def draw_ship_box(self, do_delete=False):
        """Draws the box containing the ships 
        and creates ship icons that can be dragged within it"""
        pass

    def draw_laptop(self, player_number):
        """Draws the laptop associated with the player number given.
        Will show an animation of the laptop being pulled up
        @param player_number: integer (1, 2) representing player's laptop to display"""
        pass

    def get_ship_placements(self):
        """Gets the pandas array representing the current laptop's ship placements
        @return: pandas array representing current ship placements"""
        pass

    def draw_switch_screen(self, end_player):
        """Screen to ask the players to switch the laptop"""
        pass

    def draw_shot_result(self, result):
        """draws either miss, hit, sunk screen based on result"""
        pass

    def draw_gameover(self):
        """obvious"""
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
