"""
UIDriver.py
Authors:
    - Pierce Lane
    - Holden Vail
    - Katharine Swann
    - Chase Horner
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
        self.ships_choice = 1

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
        self.bgcolor = (5, 102, 141)
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
    
    def draw_go(self):
        """Draws the GO button
        @param do_delete=False: boolean, if True will remove the element"""
        #need to adjust for do_delete and not appearing on screen when main is run
        rect_color = (121, 219, 172)
    
        window_width, window_height = self.window.get_size()

        # Button size as a percentage of the window size
        rect_width = int(window_width * 0.2)   # 20% of the window's width
        rect_height = int(window_height * 0.1)  # 10% of the window's height

        # Calculate position to center the button
        go_x = int(window_width * 0.5) - rect_width // 2
        go_y = int(window_height * 0.75)- rect_height // 2  #75% down from the top

        #Add an offset gray rectangle for shadow effect
        pygame.draw.rect(self.window, (100, 100, 100) , (go_x + 5, go_y + 5, rect_width, rect_height), border_radius=10)

        # Main rectangle with rounded corners
        pygame.draw.rect(self.window, rect_color, (go_x, go_y, rect_width, rect_height), border_radius=10)

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

    def go_clicked(self, mouse_x, mouse_y):
        """
        Check if Go button is clicked. To be used in an if statement.
        @param mouse_x: x-coordinate of the mouse click
        @param mouse_y: y-coordinate of the mouse click
        @return: True if the Go button was clicked, False otherwise
        """
        # Get the dimensions of the window
        window_width, window_height = self.window.get_size()

        # Button size as a percentage of the window size
        rect_width = int(window_width * 0.2)   # 20% of the window's width
        rect_height = int(window_height * 0.1)  # 10% of the window's height

        # Calculate position to center the button
        go_x = int(window_width * 0.5) - rect_width // 2
        go_y = int(window_height * 0.75) - rect_height // 2  # 80% down from the top

        # Check if the mouse click is within the button's rectangle
        return (go_x <= mouse_x <= go_x + rect_width) and (go_y <= mouse_y <= go_y + rect_height)
    
    def draw_title(self):
        """Draws the title text
        @param do_delete=False: boolean, if True will remove the element"""
        # first set font
        font = pygame.font.SysFont("Comic Sans MS", 300)
        # create a surface to render
        text_surface = font.render("Battleship", False, (255, 255, 255))
        # set the destination of the surface
        text_rect = text_surface.get_rect(center=(self.width/2, 200))


        self.window.blit(text_surface, text_rect)   
        # Update the display to reflect the changes
        pygame.display.update()

    def draw_ship_nums(self):
        """Draws the ship number edit control
        @param do_delete=False: boolean, if True will remove the element"""
                #Draw spindown selector
        rect_color = (121, 219, 172)
        rect_width = 75
        rect_height = 100
        rect_x = int(self.width * 0.5)- rect_width // 2
        rect_y = int(self.height * 0.55)- rect_height // 2

        #Add an offset gray rectangle for shadow effect
        pygame.draw.rect(self.window, (100, 100, 100) , (rect_x + 5, rect_y + 5, rect_width, rect_height), border_radius=10)

        # Main rectangle with rounded corners
        pygame.draw.rect(self.window, rect_color, (rect_x, rect_y, rect_width, rect_height), border_radius=10)

        #Add the text of ships_choice to the spindown selector rectangle
        font = pygame.font.SysFont("Arial", 50)
        text_surface = font.render(str(self.ships_choice), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        self.window.blit(text_surface, text_rect)

        #Add the text instructions above spindown selector rectangle
        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(str("Select Number of Ships:"), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(int(self.width * 0.5), int(self.height * 0.4)))
        self.window.blit(text_surface, text_rect)

       #Draw ship increase button by calling draw_button function
        increase_button_center = (rect_x + rect_width + 50, rect_y)
        self.draw_button(self.window, increase_button_center, 30, "▲", (2, 195, 154), (255, 255, 255))

        #Draw ship decrease button
        decrease_button_center = (rect_x + rect_width + 50, rect_y + rect_height)
        self.draw_button(self.window, decrease_button_center, 30, "▼", (2, 195, 154), (255, 255, 255))

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
        self.window.fill(self.bgcolor)        
        font = pygame.font.SysFont("Arial", 240, bold=True)
        text_surface = font.render("GAME OVER.", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        self.window.blit(text_surface, text_rect)

    def draw_main_menu(self):
        """Draws the main menu and handles events"""

        #Draw the large "BATTLESHIP" Title
        font = pygame.font.SysFont("Arial", 100, bold=True)
        text_surface = font.render("BATTLESHIP", True, (240, 243, 189))
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        text_rect.y -= 200  # move the title up
        self.window.blit(text_surface, text_rect)

        #Update the display
        pygame.display.update()


    def draw_button(self, surface, center, radius, symbol, button_color, text_color):
        """Draws circle with symbol button for main_menu"""
        #Draw offset circle for shadow effect
        pygame.draw.circle(surface, (100, 100, 100), (center[0] + 5, center[1] + 5), radius)

        #Draw actual button circle
        pygame.draw.circle(surface, button_color, center, radius)

        #Add symbol to center of circle symbol
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text_surface = font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        surface.blit(text_surface, text_rect)

    
    def up_button_clicked(self, mouse_x, mouse_y):
        rect_width = 75
        rect_height = 100
        rect_x = int(self.width * 0.5)- rect_width // 2
        rect_y = int(self.height * 0.55)- rect_height // 2
        increase_button_center = (rect_x + rect_width + 50, rect_y)
        if ((mouse_x - increase_button_center[0]) ** 2 + (mouse_y - increase_button_center[1]) ** 2) ** 0.5 <= 30:
            #increments ships_choice
            self.ships_choice = (self.ships_choice + 1 if self.ships_choice < 5 else 1)
            # Redraw to show updated choice
            self.draw_ship_nums() 
            pygame.display.update()


    def down_button_clicked(self, mouse_x, mouse_y):
        rect_width = 75
        rect_height = 100
        rect_x = int(self.width * 0.5)- rect_width // 2
        rect_y = int(self.height * 0.55)- rect_height // 2
        decrease_button_center = (rect_x + rect_width + 50, rect_y + rect_height)
        if ((mouse_x - decrease_button_center[0]) ** 2 + (mouse_y - decrease_button_center[1]) ** 2) ** 0.5 <= 30:
            #increments ships_choice
            self.ships_choice = (self.ships_choice - 1 if self.ships_choice > 1 else 5)
            # Redraw to show updated choice
            self.draw_ship_nums()
            pygame.display.update()

    def erase(self):
        self.window.fill(self.bgcolor)
        pygame.display.update()
   



