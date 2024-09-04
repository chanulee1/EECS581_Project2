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
        pygame.font.init()
        display_info = pygame.display.Info()

        # calculates the size of the window we want to initialize
        self.width = display_info.current_w * 0.8
        self.height = display_info.current_h * 0.8

        # initializes the window using the previously calculated sizes
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # define and set background color
        self.bgcolor = (0, 0, 100)
        self.window.fill(self.bgcolor) # royal blue background

        # sets the title of the window
        pygame.display.set_caption("Battleship")
        pygame.display.flip()
        log("UIDriver.__init__(self): Window initialized successfully")

        # add icon to pygame  
        self.icon_path = "./assets/battleshipLogo.jpeg"
        self.icon = pygame.image.load(self.icon_path)
        pygame.display.set_icon(self.icon)
        

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
        #need to adjust for do_delete and not appearing on screen when main is run
        rect_color = (255, 255, 255)
    
        window_width, window_height = self.window.get_size()

        # Button size as a percentage of the window size
        rect_width = int(window_width * 0.2)   # 20% of the window's width
        rect_height = int(window_height * 0.1)  # 10% of the window's height

        # Calculate position to center the button
        go_x = int(window_width * 0.5) - rect_width // 2
        go_y = int(window_height * 0.6)  #60% down from the top

        pygame.draw.rect(self.window, rect_color, (go_x, go_y, rect_width, rect_height))

        font_size = int(rect_height * 0.7)  #font = 70% of text
        font = pygame.font.SysFont("Arial", font_size)
        go_button = "GO"
        text_surface = font.render(go_button, True, (0, 0, 0))

        #center text in button
        text_rect = text_surface.get_rect(center=(go_x + rect_width // 2, go_y + rect_height // 2))
        self.window.blit(text_surface, text_rect)

        log("Go Button Drawn")

        # Update the display to show the button
        pygame.display.update()

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

    def draw_main_menu(self, ships_choice = 1):
        """Draws the main menu and handles events"""

        # draw the large title
        font = pygame.font.SysFont("Arial", 100, bold=True)
        text_surface = font.render("BATTLESHIP", True, (255, 165, 0))
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        text_rect.y -= 200  # move the title up
        self.window.blit(text_surface, text_rect)

        # draw spindown selector
        # draw a small white rectangle
        rect_color = (255, 255, 255)
        rect_width = 75
        rect_height = 100
        rect_x = self.width/2 - rect_width/2
        rect_y = self.height/2 - rect_height/2
        pygame.draw.rect(self.window, rect_color, (rect_x, rect_y, rect_width, rect_height))

        # draw the text
        font = pygame.font.SysFont("Arial", 50)
        text_surface = font.render(str(ships_choice), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        self.window.blit(text_surface, text_rect)

       # Draw ship increase button
        increase_button_color = (255, 255, 255)
        increase_button_width = 50
        increase_button_height = 50
        increase_button_x = rect_x + rect_width + 20
        increase_button_y = rect_y + rect_height / 2 - increase_button_height / 2 - 30
        pygame.draw.polygon(self.window, increase_button_color, [
            (increase_button_x, increase_button_y + increase_button_height),
            (increase_button_x + increase_button_width / 2, increase_button_y),
            (increase_button_x + increase_button_width, increase_button_y + increase_button_height)
        ], 0)

        # Draw ship decrease button
        decrease_button_color = (255, 255, 255)
        decrease_button_width = 50
        decrease_button_height = 50
        decrease_button_x = rect_x + rect_width + 20
        decrease_button_y = rect_y + rect_height / 2 - decrease_button_height / 2 + 30
        pygame.draw.polygon(self.window, decrease_button_color, [
            (decrease_button_x, decrease_button_y),
            (decrease_button_x + decrease_button_width / 2, decrease_button_y + decrease_button_height),
            (decrease_button_x + decrease_button_width, decrease_button_y)
        ], 0)

        # Update the display
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # Check if increase button is clicked
                    if (increase_button_x <= mouse_x <= increase_button_x + increase_button_width and
                            increase_button_y <= mouse_y <= increase_button_y + increase_button_height):
                        ships_choice = (ships_choice + 1 if ships_choice < 5 else 1)
                        self.draw_main_menu(ships_choice)  # Redraw to show updated choice

                    # Check if decrease button is clicked
                    if (decrease_button_x <= mouse_x <= decrease_button_x + decrease_button_width and
                            decrease_button_y <= mouse_y <= decrease_button_y + decrease_button_height):
                        ships_choice = (ships_choice - 1 if ships_choice > 1 else 5)
                        self.draw_main_menu(ships_choice)  # Redraw to show updated choice
            # Update the display
                pygame.display.update()
        pygame.quit()

