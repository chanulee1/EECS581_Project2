"""
UIDriver.py
Authors:
    - Pierce Lane
    - Holden Vail
    - Katharine Swann
    - Chase Horner
    - Michael Stang
Date: 9/2/2024

Purpose: drives the UI of the battleship game
"""
from Logger.Logger import *
import pygame
# temp import
from time import sleep
from UI.TugBoat import *

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
        self.clock = pygame.time.Clock()

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
    
    def draw_go(self, surface = None):
        """Draws the GO button
        @param do_delete=False: boolean, if True will remove the element"""
        #need to adjust for do_delete and not appearing on screen when main is run
        rect_color = (121, 219, 172)
        surface = (self.window if surface == None else surface)
        window_width, window_height = surface.get_size()

        # Button size as a percentage of the window size
        rect_width = int(window_width * 0.2)   # 20% of the window's width
        rect_height = int(window_height * 0.1)  # 10% of the window's height

        # Calculate position to center the button
        go_x = int(window_width * 0.5) - rect_width // 2
        go_y = int(window_height * 0.75)- rect_height // 2  #75% down from the top

        #Add an offset gray rectangle for shadow effect
        pygame.draw.rect(surface, (100, 100, 100) , (go_x + 5, go_y + 5, rect_width, rect_height), border_radius=10)

        # Main rectangle with rounded corners
        pygame.draw.rect(surface, rect_color, (go_x, go_y, rect_width, rect_height), border_radius=10)

        font_size = int(rect_height * 0.7)  #font = 70% of text
        font = pygame.font.SysFont("Arial", font_size)
        go_button = "GO"
        text_surface = font.render(go_button, True, (0, 0, 0))

        #center text in button
        text_rect = text_surface.get_rect(center=(go_x + rect_width // 2, go_y + rect_height // 2))
        surface.blit(text_surface, text_rect)

        log("Go Button Drawn")

        # Update the display to show the button
        pygame.display.update()

    #TODO rewrite go button with collidepoint instead of go_clicked
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

        #Add the text of ship_count to the spindown selector rectangle
        font = pygame.font.SysFont("Arial", 50)
        text_surface = font.render(str(self.ship_count), True, (0, 0, 0))
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

    def draw_ship_box(self):
        """Draws the box containing the ships 
        and creates ship icons that can be dragged within it"""
         # Create a background buffer which holds the static objects to be repeatedly merged onto the dynamic window
        background = pygame.Surface((self.width, self.height))
        background.fill(self.bgcolor)
        self.draw_go(background)
 
        #Draw white square based on number of ships selected
        rect_color = (255, 255, 255)
        rect_width = 100 * self.ship_count + 10
        rect_height = 100 * self.ship_count + 10
        rect_x = int(self.width * 0.25)- rect_width // 2
        rect_y = int(self.height * 0.4)- rect_height // 2
        pygame.draw.rect(background, rect_color, (rect_x, rect_y, rect_width, rect_height), border_radius=25)

        #draw another box in bg_color to make it a white outline
        rect_width = 100 * self.ship_count
        rect_height = 100 * self.ship_count
        rect_x = int(self.width * 0.25)- rect_width // 2
        rect_y = int(self.height * 0.4)- rect_height // 2
        pygame.draw.rect(background, self.bgcolor, (rect_x, rect_y, rect_width, rect_height), border_radius=25)
        
        #Makes a list of tug_boat (draggable boat) objects, spaced evenly throughout the white box
        tug_boats = []
        for ship_size in range(1, self.ship_count+1):
            x = rect_x + 10
            y = rect_y + 10 + 100 * (ship_size-1)
            tug_boat = TugBoat(x, y, ship_size, self.window)
            tug_boats.append(tug_boat)

        # To keep track of the currently dragged object
        dragged_object = None  

        #Loop to keep updating the screen until GO is clicked
        #TODO Make sure GO cannot be clicked until all ships are placed
        waiting = True
        all_ships_placed = True #This should eventually start as false
        while waiting:
            #typical quit procedure
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                #At every Mouse down, checks if it collides with each tugboat (ie the boat was clicked on)
                #If it is clicked, sets dragging to True and sets dragged_object and breaks loop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for tug_boat in tug_boats:
                        if tug_boat.rect.collidepoint(mouse_x, mouse_y):
                            tug_boat.dragging = True
                            dragged_object = tug_boat
                            break
                    if self.go_clicked(mouse_x, mouse_y) and all_ships_placed:
                        waiting = False

                #On mouse up events, if a boat is being drag, stop dragging it (set dragging to false and clear dragged_object)
                if event.type == pygame.MOUSEBUTTONUP:
                    if dragged_object:
                        dragged_object.dragging = False
                        dragged_object = None  

            #Clear the screen with the background buffer
            self.window.blit(background, (0, 0))

            #Update the x,y position of the currently dragged object
            if dragged_object:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dragged_object.update(mouse_x, mouse_y)

            #Draw all TugBoat objects
            for tug_boat in tug_boats:
                tug_boat.draw()

            #Update the display
            pygame.display.update()

            #Cap the frame rate
            self.clock.tick(60)



    def draw_laptop(self, player_number):
        """Draws the laptop associated with the player number given.
        Will show an animation of the laptop being pulled up
        @param player_number: integer (1, 2) representing player's laptop to display"""
        pass

    def draw_grids(self):
        """A test function used to draw two grids, we can use these for laptops if we want, but it gives a start"""
        
        # Declares it a 10x10
        GRID_ROWS = 10
        GRID_COLS = 10

        # Size of each box
        GRID_SIZE = 30

        # Loops to create a grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect((self.width/2) - (GRID_SIZE * 5) + col * GRID_SIZE, (self.height/2) + (self.height/4) - (GRID_SIZE * 5) + row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.window, (255, 255, 255), rect, 1)
        
        # Updates view
        pygame.display.update()
    
    def tile_clicked(self, mouse_x, mouse_y):
        """Turns a mouse x and mouse y into grid coordinates for bottom grid
        @param int mouse_x: The x position of where the click occured
        @param int mouse_y: The y position of where the click occured
        @return (int, string): Returns a standard coord for this program"""
        TILE_SIZE = 30

        # Calculates x position by using the mouse position and adjusting for where the grid is.
        x_pos = mouse_x - ((self.width/2) - (TILE_SIZE * 5))

        # Calculates y position by using mouse position adjusting for where grid is up and down.
        y_pos = mouse_y - ((self.height * 3/4) - (TILE_SIZE * 5))

        # Turns x and y position into X,Y positions
        x_coord = int((x_pos // 30) + 1)
        y_coord = int((y_pos // 30) + 1)

        # Conversion dictonary to help turn ints int letters
        conversion = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "F", "7": "G", "8": "H", "9": "I", "10": "J"}

        # Returns the coord of the click in our format for coords (row int, column letter string)
        return (y_coord, conversion[str(x_coord)])

    def get_ship_placements(self):
        """Gets the pandas array representing the current laptop's ship placements
        @return: pandas array representing current ship placements"""
        pass

    def draw_switch_screen(self, end_player):
        """Screen to ask the players to switch the laptop"""
        self.erase()

        #Draw the large "Player __ Turn" Title
        font = pygame.font.SysFont("Arial", 100, bold=True)
        text_surface = font.render(f"Player {end_player}'s Turn", True, (240, 243, 189))
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        text_rect.y -= 200  # move the title up
        self.window.blit(text_surface, text_rect)

        self.draw_go()

        #Update the display
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                #Stores the mouse position for every click to determine if a button was clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    waiting = not self.go_clicked(mouse_x, mouse_y)

        self.erase()
        return

    def draw_shot_result(self, result):
        """draws either miss, hit, sunk screen based on result"""
        pass

    def draw_gameover(self):
        """obvious"""
        self.window.fill(self.bgcolor)
        font_size = int(self.height * 0.3) #adjusts font size to 0.3 of height       
        font = pygame.font.SysFont("Arial", font_size, bold=True) #set font with size
        text_surface = font.render("GAME OVER.", True, (255, 0, 0)) #color = red rn
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        self.window.blit(text_surface, text_rect) #draw the text
        pygame.display.update()  #update the display

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
            #increments ship_count
            self.ship_count = (self.ship_count + 1 if self.ship_count < 5 else 1)
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
            #increments ship_count
            self.ship_count = (self.ship_count - 1 if self.ship_count > 1 else 5)
            # Redraw to show updated choice
            self.draw_ship_nums()
            pygame.display.update()

    def erase(self):
        self.window.fill(self.bgcolor)
        pygame.display.update()
   



