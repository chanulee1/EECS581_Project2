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
from time import sleep
from UI.TugBoat import *
from UI.Laptop import *

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

        # Calculates the size of the window we want to initialize
        self.width = display_info.current_w * 0.8
        self.height = display_info.current_h * 0.8

        # Initializes the window using the previously calculated sizes
        self.window = pygame.display.set_mode((self.width, self.height))

        # Define and set background color
        self.bgcolor = (17, 116, 175)
        self.window.fill(self.bgcolor)

        # Adding in pre-designed background image for main menu
        self.bg_image_path = "./assets/background.png"
        self.bg_image = pygame.image.load(self.bg_image_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height)) 
        # Scale the image to fit window

        self.window.blit(self.bg_image, (0, 0))

        # Sets the title of the window
        pygame.display.set_caption("Battleship")
        pygame.display.flip()
        log("UIDriver.__init__(self): Window initialized successfully")

        # Add icon to pygame  
        self.icon_path = "./assets/battleshipLogo.jpeg"
        self.icon = pygame.image.load(self.icon_path)
        pygame.display.set_icon(self.icon)
        

        # Define uninitialized class variables
        # p1 laptop object
        self.p1_laptop = Laptop(1, self.width, self.height, tile_size = 40)   
        # p2 laptop object
        self.p2_laptop = Laptop(2, self.width, self.height, tile_size = 40)
        # Member variable to see which laptop is currently being displayed
        self.cur_laptop = None
        # Go button object
        self.go_button = None   
        # Number of ships locked in via main menu
        self.ship_count = 3     

    
    def wait_for_go(self, ship_num_menu = False):
        """Waits for the go button to be pressed.
        Assumes that the go button exists

        @param ship_num_menu = False: bool that adds some extra checks in the ship num menu"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                    # Quits if event type is quit
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    # Stores the mouse position for every click to determine if a button was clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos

                        # Check if increase button is clicked, which is determined by is_button_clicked function
                        if (ship_num_menu):
                            self.up_button_clicked(mouse_x, mouse_y)
                            self.down_button_clicked(mouse_x, mouse_y)
                        waiting = not self.go_clicked(mouse_x, mouse_y)

    def draw_go(self, surface = None):
        """Draws the GO button
        
        @param do_delete=False: boolean, if True will remove the element"""

        rect_color = (16, 64, 128) # Dark blue
        surface = (self.window if surface == None else surface)
        window_width, window_height = surface.get_size()

        # Button size as a percentage of the window size
        rect_width = int(window_width * 0.2)   # 20% of the window's width
        rect_height = int(window_height * 0.1)  # 10% of the window's height

        # Calculate position to center the button
        go_x = int(window_width * 0.5) - rect_width // 2
        go_y = int(window_height * 0.75)- rect_height // 2  # 75% down from the top

        # Add an offset gray rectangle for drop shadow effect
        pygame.draw.rect(surface, (0, 0, 0) , (go_x + 5, go_y + 5, rect_width, rect_height), border_radius=10)

        # Main rectangle with rounded corners
        pygame.draw.rect(surface, rect_color, (go_x, go_y, rect_width, rect_height), border_radius=10)

        font_size = int(rect_height * 0.7)  # Font = 70% of text
        font = pygame.font.SysFont("Arial", font_size)
        go_button = "GO"
        text_surface = font.render(go_button, True, (255, 255, 255))

        # Center text in button
        text_rect = text_surface.get_rect(center=(go_x + rect_width // 2, go_y + rect_height // 2))
        surface.blit(text_surface, text_rect)

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

    def draw_ship_nums(self):
        """Draws the ship number edit control
        
        @param do_delete=False: boolean, if True will remove the element"""
        # Draw spindown selector
        rect_color = (16, 64, 128)
        rect_width = 75
        rect_height = 100
        rect_x = int(self.width * 0.5)- rect_width // 2
        rect_y = int(self.height * 0.55)- rect_height // 2

        # Add an offset gray rectangle for shadow effect
        pygame.draw.rect(self.window, (0, 0, 0) , (rect_x + 5, rect_y + 5, rect_width, rect_height), border_radius=10)

        # Main rectangle with rounded corners
        pygame.draw.rect(self.window, rect_color, (rect_x, rect_y, rect_width, rect_height), border_radius=10)

        # Add the text of ship_count to the spindown selector rectangle
        font = pygame.font.SysFont("Arial", 50)
        text_surface = font.render(str(self.ship_count), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        self.window.blit(text_surface, text_rect)

        # Add the text instructions above spindown selector rectangle
        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(str("Select Number of Ships:"), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.width * 0.5), int(self.height * 0.4)))
        self.window.blit(text_surface, text_rect)

       # Draw ship increase button represented by a plus sign (+)
        increase_button_center = (rect_x + rect_width + 50, rect_y)
        self.draw_button(self.window, increase_button_center, 30, "+", (16, 64, 128), (255, 255, 255))

        # Draw ship decrease button represented by a minus sign (-)
        decrease_button_center = (rect_x + rect_width + 50, rect_y + rect_height)
        self.draw_button(self.window, decrease_button_center, 30, "-", (16, 64, 128), (255, 255, 255))

    def draw_ship_box(self, player_number = 1):
        """Draws the box containing the ships 
        and creates ship icons that can be dragged within it
        
        @param player_number: int (1, 2) tracking which player's ship box is being drawn"""

        ship_positions = dict()
        taken_positions = set()

         # Create a background buffer which holds the static objects to be repeatedly merged onto the dynamic window
        background = pygame.Surface((self.width, self.height))
        background.fill(self.bgcolor)
        self.draw_go(background)
 
        tugboat_spacer = TugBoat.tile_size+20

        # Draw white square based on number of ships selected
        rect_color = (255, 255, 255)
        rect_width = tugboat_spacer * self.ship_count + 10
        rect_height = tugboat_spacer * self.ship_count + 10
        rect_x = int(self.width * 0.15)- rect_width // 2
        rect_y = int(self.height * 0.80)- rect_height // 2
        pygame.draw.rect(background, rect_color, (rect_x, rect_y, rect_width, rect_height), border_radius=25)

        # Draw another box in bg_color to make it a white outline
        rect_width = tugboat_spacer * self.ship_count
        rect_height = tugboat_spacer * self.ship_count
        rect_x = int(self.width * 0.15)- rect_width // 2
        rect_y = int(self.height * 0.80)- rect_height // 2
        pygame.draw.rect(background, self.bgcolor, (rect_x, rect_y, rect_width, rect_height), border_radius=25)
        
        # Makes a list of tug_boat (draggable boat) objects, spaced evenly throughout the white box
        tug_boats = []
        for ship_size in range(1, self.ship_count+1):
            x = rect_x + 10
            y = rect_y + 10 + tugboat_spacer * (ship_size-1)
            tug_boat = TugBoat(x, y, ship_size, self.window)
            tug_boats.append(tug_boat)

        # To keep track of the currently dragged object
        dragged_object = None  

        # Loop to keep updating the screen until GO is clicked
        waiting = True
        while waiting:
            # Typical quit procedure
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # At every Mouse down, checks if it collides with each tugboat (ie the boat was clicked on)
                # If it is clicked, sets dragging to True and sets dragged_object and breaks loop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for tug_boat in tug_boats:
                        if tug_boat.rect.collidepoint(mouse_x, mouse_y):
                            tug_boat.dragging = True
                            dragged_object = tug_boat
                            # Remove from positions taken when placing to not stop slight movements
                            
                            if dragged_object.size in ship_positions.keys():
                                for i in range(dragged_object.size):
                                    if dragged_object.is_horizontal:
                                        coord = (ship_positions[dragged_object.size][0][0], chr(ord(ship_positions[dragged_object.size][0][1])+i))
                                    else:
                                        coord = (ship_positions[dragged_object.size][0][0]+i, ship_positions[dragged_object.size][0][1])
                                    
                                    if coord in taken_positions:
                                        taken_positions.remove(coord)
                                
                                ship_positions.pop(dragged_object.size)
                            break
                    if self.go_clicked(mouse_x, mouse_y) and len(ship_positions.keys()) == len(tug_boats):
                        waiting = False

                ## CODE FOR SNAP TO GRID ##
                
                # On mouse up events, if a boat is being drag, stop dragging it (set dragging to false and clear dragged_object)
                # Then snap grid to nearest grid tiles
                if event.type == pygame.MOUSEBUTTONUP:
                    if dragged_object:
                        # Important to note, all ship snapping is handled by the "head" of the ship, which is the top left corner

                        # Constant grid size for math on snapping
                        GRID_SIZE = 40 

                        # Marks the upper left of the placement grid
                        grid_upper_left_x = (self.width/2) - (GRID_SIZE * 5)
                        grid_upper_left_y = (self.height/3) - (GRID_SIZE * 5)

                        # Gets the current position of the block as its being "Dropped"
                        before_x, before_y = dragged_object.rect.topleft

                        # Calculates which column and row the upper left is closest to
                        column_to_snap = round(((before_x) - grid_upper_left_x)/GRID_SIZE)
                        row_to_snap = round(((before_y) - grid_upper_left_y)/GRID_SIZE)

                        # The highest index of columns and rows (in this case there are 10 rows 
                        # and 10 columns indexed [for now] as 0-9)
                        max_column = 9
                        max_row = 9

                        # Based on the orientation of the ship, reduces the range of viable coordinates that a ship's 
                        # head can be placed to ensure all pieces are in the 10x10 if the ship is horizontal
                        if dragged_object.is_horizontal:
                            # We reduce the column range to 0 through 9 - length of ship + 1
                            max_column -= dragged_object.size - 1
                        else:
                            # Same as above, but with rows if the ship is vertical
                            max_row -= dragged_object.size - 1

                        # Checks if the ship is outside of the bounds of the grid, and if so, adjusts to put it onto the placement grid
                        # If the column is calculated as above the highest column is allowed and is set to the max
                        # Leads to the ships "snapping" to the outside edge if you drag it outside of the 10x10
                        if column_to_snap > max_column:
                            column_to_snap = max_column
                        
                        # Same as above but with row.
                        # It IS possible that it snaps to the max of both columns and rows, so these can't be elifs
                        if row_to_snap > max_row:
                            row_to_snap = max_row

                        # Checks if the columnn is below 0 (to the left of the grid)
                        if column_to_snap < 0:
                            column_to_snap = 0

                        # Checks if the rows is below 0 (above the grid)
                        if row_to_snap < 0:
                            row_to_snap = 0

                        # Moves the ship to snap position
                        # Force move forced a ship into a position by setting its UPPER LEFT corner
                        # This takes the upper left of the grid and adds a multiple of the grid size to put it into the correct position
                        dragged_object.force_move(grid_upper_left_x + GRID_SIZE * column_to_snap,grid_upper_left_y + GRID_SIZE * row_to_snap)

                        # Marks where the head of the ship is so we can mark it
                        head_position = (row_to_snap+1, chr(ord('A') + column_to_snap))

                        # Checks whether the ship is currently horizontal or vertical
                        if dragged_object.is_horizontal:
                            # Calculates the tail by using the size and which orientation it's in
                            tail_position = (row_to_snap + 1, chr(ord('A') + column_to_snap + dragged_object.size - 1))
                        else:
                            # Same as above but if it's vertical
                            tail_position = (row_to_snap + dragged_object.size, chr(ord('A') + column_to_snap))
                        
                        # Variable to hold all of the coordinates between the head and tail (inclusive)
                        coords_to_add = set()
                        # Variable to hold whether or not there is an overlap
                        overlap = False

                        # Loops a number of times equal to the number of tiles the ship is
                        for i in range(dragged_object.size):

                            # If it's currently horizontal
                            if dragged_object.is_horizontal:
                                # Goes tile by tile right
                                coord = (head_position[0], chr(ord(head_position[1])+i))
                            else:
                                # Otherwise goes tile by tile down
                                coord = (head_position[0]+i, head_position[1])
                            
                            # If the coordinate we calculated is already in the set of taken_positions then there is already a ship there
                            # We remove a ship's coordinates from taken_positions when its picked up, so there shouldn't be any issues with a ship
                            # seeing its own coordinates
                            if coord in taken_positions:
                                
                                # If the object is vertical we have to rotate it back to horizontal before we move back to the ship box
                                if not dragged_object.is_horizontal:
                                    dragged_object.rotate()
                                
                                # Force the ship object back to where it was created
                                dragged_object.force_move(dragged_object.original_pos[0], dragged_object.original_pos[1])

                                # Flips our indicator variable that there was an overlap to ensure it's not added to the taken positions/ship placements
                                overlap = True

                                # Breaks out of loop once we find the FIRST overlap
                                break

                            else:

                                # If there's no overlap, we simple add the coordinate to our temporary set that holds all of the coords for the 
                                # currently-being-dropped ship
                                coords_to_add.add(coord)

                            # If there were NO overlaps
                            if not overlap:
                                # Go through the temporary set and add it to the taken positions
                                for internal_coord in coords_to_add:
                                    taken_positions.add(internal_coord)

                                # Then add the ship to dictonary for tracking which ships have been placed
                                ship_positions[dragged_object.size] = (head_position, tail_position)
                        
                        # Stop dragging the boat
                        dragged_object.dragging = False
                        dragged_object = None
                        

                # On the correct keydown event, rotate the ship
                if event.type == pygame.KEYDOWN:
                    # If a boat is being dragged and the "r" key is pressed
                    if dragged_object is not None and event.key == pygame.K_r:
                            dragged_object.rotate()
                    

            # Clear the screen with the background buffer
            self.window.blit(background, (0, 0))

            # Update the x,y position of the currently dragged object
            if dragged_object:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dragged_object.update(mouse_x, mouse_y)

            # Draw all TugBoat objects
            for tug_boat in tug_boats:
                tug_boat.draw()

            # Draw the placement grid
            self.draw_grid()

            # Update the display
            pygame.display.update()

            # Cap the frame rate
            self.clock.tick(60)
        
        return ship_positions.values()
        
    def draw_laptop(self, gamestate):
        """Draws the laptop associated with the player whose turn it is.
        Will show an animation of the laptop being pulled up

        @param Gamestate: To draw the current boards
        @raise ValueError: player_number != 1 or 2"""

        ## Draw the laptop grids

        # First define which laptop we should be drawing
        player_number = gamestate.turn
        if player_number == 1: # Player 1
            self.cur_laptop = self.p1_laptop
        elif player_number == 2: # Player 2
            self.cur_laptop = self.p2_laptop
        else: # Only allow for 2 players
            raise ValueError("Invalid player number")
        
        # Grab the friendly and enemy boards from GameState
        friendly_df = gamestate.friendly_board()
        enemy_df = gamestate.enemy_board()

        # Loop through rows and cols of each grid
        for row in range(Laptop.SIZE_Y):
            for col in range(Laptop.SIZE_X):
                # Converts col to corresponding character 1-> 'A', etc...
                str_col = chr(65 + col)

                # Grab our grid's tile
                our_tile = self.cur_laptop.our_grid[row][col]
                # Grab the top left coordinate in pixels
                left = our_tile.top_left[0]
                top = our_tile.top_left[1]
                # Create a rectangle at those coordinates
                rect = pygame.Rect(left, top, self.cur_laptop.tile_size, self.cur_laptop.tile_size)
                # Checks the GameState board at that spot
                friendly_square = friendly_df.loc[row+1, str_col]
                # Draws the status of the gs board
                color = ((255,0,0) if '*' in friendly_square 
                         else (100,100,100) if friendly_square in '12345'
                         else (255,255,255) if friendly_square == 'M'
                         else (73, 160, 169))
                pygame.draw.rect(self.window, color, rect)
                # Draw border
                pygame.draw.rect(self.window, (255, 255, 255), rect, 1)

                # Grab their grid's tile
                their_tile = self.cur_laptop.their_grid[row][col]
                # Grab the top left coordinate in pixels
                left = their_tile.top_left[0]
                top = their_tile.top_left[1]
                # Create a rectangle at those coordinates
                rect = pygame.Rect(left, top, self.cur_laptop.tile_size, self.cur_laptop.tile_size)
                # Checks the Gamestate board at that spot
                enemy_square = enemy_df.loc[row+1, str_col]
                # Draws the status of the gs board except for unhit ships
                color = ((255,0,0) if '*' in enemy_square 
                         else (255,255,255) if enemy_square == 'M'
                         else (73, 160, 169))
                pygame.draw.rect(self.window, color, rect)
                # Draw border
                pygame.draw.rect(self.window, (255, 255, 255), rect, 1)

        # Title for our grid
        font = pygame.font.SysFont("Arial", 50, bold=True)
        title_text_our = font.render("Friendly Ships", True, (255, 255, 255))
        title_rect_our = title_text_our.get_rect(center=(self.cur_laptop.our_grid[0][0].top_left[0] + self.cur_laptop.tile_size * Laptop.SIZE_X / 2, 40))
        self.window.blit(title_text_our, title_rect_our)

        # Title for their grid
        title_text_their = font.render("Enemy Ships", True, (255, 255, 255))
        title_rect_their = title_text_their.get_rect(center=(self.cur_laptop.their_grid[0][0].top_left[0] + self.cur_laptop.tile_size * Laptop.SIZE_X / 2, 40))
        self.window.blit(title_text_their, title_rect_their)

        # Add instructions on firing below thier grid
        font = pygame.font.SysFont("Arial", 30)
        instruction_text = font.render("Click a square to fire!", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(
            self.cur_laptop.their_grid[0][0].top_left[0] + self.cur_laptop.tile_size * Laptop.SIZE_X / 2, 
            self.cur_laptop.their_grid[0][0].top_left[1] + self.cur_laptop.tile_size * Laptop.SIZE_Y + 40))       
        self.window.blit(instruction_text, instruction_rect)

        # Update the display
        pygame.display.update()


    def wait_for_shot(self, gamestate):
        """
        # waits for UI input and returns what square was clicked.
     
        @return: (int, str) of which square is being targetted
        """
        # Draws the laptops and legends
        self.draw_laptop(gamestate)
        self.draw_legends()
        log('Laptop Drawn')
        
        # Loops until a successful click
        while True:
            for event in pygame.event.get():
                    # Quits if event type is quit
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    # Stores the mouse position for every click to determine if a button was clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos

                        # Iterates over every tile
                        for row in range(Laptop.SIZE_Y):
                            for col in range(Laptop.SIZE_X):
                                # Converts col to corresponding character 1-> 'A', etc...
                                str_col = chr(65 + col)

                                # Grab thier grid's tile
                                tile = self.cur_laptop.their_grid[row][col]
                                # Checks if the tile is even clickable (not already shot at) and if the click is within the tiles range
                                if tile.clickable and (tile.top_left[0]<=mouse_x<=tile.bottom_right[0]) and (tile.top_left[1]<=mouse_y<=tile.bottom_right[1]):
                                    # Now the tile is no clickable
                                    tile.clickable = False
                                    # Return (int, str) coordinate of which tile was shot at
                                    return((row+1, str_col))


    def draw_grid(self):
        """Draws the ship placement grid, uses its own thing instead of Laptop.py
        Also draws the Press R To Rotate text"""
        
        # Declares it a 10x10
        GRID_ROWS = 10
        GRID_COLS = 10

        # Size of each box
        GRID_SIZE = self.p1_laptop.tile_size

        left = self.width/2 - GRID_SIZE*5
        top = self.height/3 - GRID_SIZE*5

        # Loops to create a grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect((self.width/2) - (GRID_SIZE * 5) + col * GRID_SIZE, (self.height/3) - (GRID_SIZE * 5) + row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.window, (255, 255, 255), rect, 1)

        ## DRAW LEGEND ON SHIP PLACEMENT GRID
        font = pygame.font.SysFont("Arial", 20)
        number_x = int(left - GRID_SIZE/2)  # Starting x-coordinate for the numbers
        number_y = int(top + GRID_SIZE/2)  # Starting y-coordinate for the numbers
        
        # Draw the numbers 1-10 in a vertical bar
        for i in range(10):
            number = str(i + 1)
            text_surface = font.render(number, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(number_x, number_y))
            self.window.blit(text_surface, text_rect)
            number_y += GRID_SIZE

        # Define where the board's letters should start
        letter_x = int(left + GRID_SIZE/2)  # Starting x-coordinate for the letters
        letter_y = int(top - GRID_SIZE/2)  # Adjusted y-coordinate for the letters
        # Draw the letters A-J in a horizontal bar
        for i in range(10):
            letter = chr(ord('A') + i)  # Get the corresponding letter
            text_surface = font.render(letter, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(letter_x, letter_y))
            self.window.blit(text_surface, text_rect)
            letter_x += GRID_SIZE

        ## DRAW THE TEXT
        font = pygame.font.SysFont("Arial", 30)
        text = font.render("Press R to Rotate", True, (255, 255, 255))
        text_rect = text.get_rect(center = (letter_x + GRID_SIZE*GRID_COLS/2, letter_y + GRID_SIZE*GRID_ROWS/2))
        self.window.blit(text, text_rect)
        
        # Update the display
        pygame.display.update()

    def draw_legends(self): # Draws key on to window during game play
        """Draws the legend for the boards"""
        font = pygame.font.SysFont("Arial", 20)
        spacing = self.p1_laptop.tile_size  # Spacing between each char

        # Get the top left coordinates of the left grid
        our_left = self.p1_laptop.our_grid[0][0].top_left[0]
        our_top = self.p1_laptop.our_grid[0][0].top_left[1]

        # Get the top left coordinates of the right grid
        their_left = self.p1_laptop.their_grid[0][0].top_left[0]
        their_top = self.p1_laptop.their_grid[0][0].top_left[1]


        ## LEFT BOARD LEGENDS
        number_x = int(our_left - spacing/2)  # Starting x-coordinate for the numbers
        number_y = int(our_top + spacing/2)  # Starting y-coordinate for the numbers
        # Draw the numbers 1-10 in a vertical bar (left board)
        for i in range(10):
            number = str(i + 1)
            text_surface = font.render(number, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(number_x, number_y))
            self.window.blit(text_surface, text_rect)
            number_y += spacing

        # Define where the left board's letters should start
        letter_x = int(our_left + spacing/2)  # Starting x-coordinate for the letters
        letter_y = int(our_top - spacing/2)  # Adjusted y-coordinate for the letters
        # Draw the letters A-J in a horizontal bar (left board)
        for i in range(10):
            letter = chr(ord('A') + i)  # Get the corresponding letter
            text_surface = font.render(letter, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(letter_x, letter_y))
            self.window.blit(text_surface, text_rect)
            letter_x += spacing


        ## RIGHT BOARD LEGENDS
        # Draw the numbers 1-10 in a vertical bar (right board)
        # Define where our numbers should start
        number_x = int(their_left - spacing/2)  # Starting x-coordinate for the numbers
        number_y = int(their_top + spacing/2)  # Starting y-coordinate for the numbers
        for i in range(10):
            number = str(i + 1)
            text_surface = font.render(number, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(number_x, number_y))
            self.window.blit(text_surface, text_rect)
            number_y += spacing

        # Draw the letters A-J in a (horizontal bar)
        letter_x = int(their_left + spacing/2)  # Starting x-coordinate for the letters
        letter_y = int(their_top - spacing/2)  # Adjusted y-coordinate for the letters
        for i in range(10):
            letter = chr(ord('A') + i)  # Get the corresponding letter
            text_surface = font.render(letter, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(letter_x, letter_y))
            self.window.blit(text_surface, text_rect)
            letter_x += spacing

    # Draw each item in the legend
        legend_items = [
        ((255,255,255), "Miss"),    #White
        ((255,0,0), "Hit"),         #Red
        ((100,100,100), "Ship"),    #Gray
        ((73, 160, 169), "Water")]  #Blue

        window_width, window_height = self.window.get_size()
        x = int(window_width * 0.1) 
        y = int(window_height * 0.85)

        # Draw key text
        bigger_font = pygame.font.SysFont("Arial", 20, bold = True)
        text = bigger_font.render('Key:', True, (255,255,255))
        text_rect = text.get_rect(center=(window_width * 0.1, y - 40))
        self.window.blit(text, text_rect)

        for i, (color, label) in enumerate(legend_items):
            # Calculate positions
            pos_x = x + i * (spacing * 2 + 60)
            pos_y = y # Keep their y the same to be aligned
            
            # Draw colored square
            color_rect = pygame.Rect(pos_x, pos_y, 30, 30)
            pygame.draw.rect(self.window, color, color_rect)
            
            # Draw border around the square
            pygame.draw.rect(self.window, (0, 0, 0), color_rect, 1) # 1 is the border width
            
            # Draw label text
            text = font.render(label, True, (0, 0, 0))
            text_rect = text.get_rect(midleft=(pos_x + 40, pos_y + 15))
            self.window.blit(text, text_rect)

        # Update the display
        pygame.display.update()


    def do_text_screen(self, text):
        """Screen to ask the players to switch the laptop

        @param text: string of text to put on the screen"""
        self.erase()

        # Draw the large "text" Title
        font = pygame.font.SysFont("Arial", 100, bold=True)
        text_surface = font.render(f"{text}", True, (240, 243, 189))
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        text_rect.y -= 200  # Move the title up
        self.window.blit(text_surface, text_rect)

        self.draw_go()

        # Update the display
        pygame.display.update()

        # Wait for them to press GO
        self.wait_for_go()

        # Then reset our whole screen
        self.erase()
    
    def draw_gameover(self):
        """Draws the gameover screen
        
        @raise ValueError: if an invalid laptop is loaded into self.cur_laptop"""

        # Check who won
        if self.cur_laptop is self.p1_laptop:
            gameover_text = "Player 1 Wins!"
        elif self.cur_laptop is self.p2_laptop:
            gameover_text = "Player 2 Wins!"
        else: # Make sure to do error checking
            raise ValueError("Invalid player winning")

        self.window.fill(self.bgcolor) 
        font_size = int(self.width*.1) # Adjusts font size to be 0.1 of width
        font = pygame.font.SysFont("Arial", font_size, bold=True) # Set font with size

        text_surface_white = font.render(gameover_text, True, (255, 255, 255)) # White
        text_surface_black = font.render(gameover_text, True, (0, 0, 0))  # Black outline

        text_rect = text_surface_white.get_rect(center=(self.width / 2, self.height / 2)) # Get center for text

        drop_shadow = text_rect.copy()
        drop_shadow.x += 7
        drop_shadow.y += 7

        self.window.blit(text_surface_black, drop_shadow)
        self.window.blit(text_surface_white, text_rect)
        
        # Update the display
        pygame.display.update()

    def draw_main_menu(self):
        """Draws title on main menu page"""
        font = pygame.font.SysFont("Arial", 125, bold=True) # Font style, font size, bold
        title_text = "BATTLESHIP" # Title screen text
        text_surface_white = font.render(title_text, True, (255, 255, 255)) # White
        text_surface_black = font.render(title_text, True, (0, 0, 0))  # Black outline
    
        text_rect = text_surface_white.get_rect(center=(self.width / 2, self.height / 2))
        # Get center for text
        text_rect.y -= 230  # Move the title up

        drop_shadow = text_rect.copy()
        drop_shadow.x += 7
        drop_shadow.y += 7
        
        self.window.blit(text_surface_black, drop_shadow)
        self.window.blit(text_surface_white, text_rect)

        # Update the display
        pygame.display.update()

    def draw_button(self, surface, center, radius, symbol, button_color, text_color):
        """Draws circle with symbol button for main_menu"""
        # Draw offset circle for shadow effect
        pygame.draw.circle(surface, (0, 0, 0), (center[0] + 5, center[1] + 5), radius)

        # Draw actual button circle
        pygame.draw.circle(surface, button_color, center, radius)

        # Add symbol to center of circle symbol
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text_surface = font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        surface.blit(text_surface, text_rect)

    
    def up_button_clicked(self, mouse_x, mouse_y):
        """Checks if up button is clicked, and increments ship counter"""
        rect_width = 75
        rect_height = 100
        rect_x = int(self.width * 0.5)- rect_width // 2
        rect_y = int(self.height * 0.55)- rect_height // 2
        #Calculate the location of increase button
        increase_button_center = (rect_x + rect_width + 50, rect_y)
        if ((mouse_x - increase_button_center[0]) ** 2 + (mouse_y - increase_button_center[1]) ** 2) ** 0.5 <= 30:
            # Increments ship_count
            self.ship_count = (self.ship_count + 1 if self.ship_count < 5 else 1)
            # Redraw to show updated choice
            self.draw_ship_nums() 

            # Update the display
            pygame.display.update()


    def down_button_clicked(self, mouse_x, mouse_y):
        """Checks if down button is clicked, and decrements ship counter"""
        rect_width = 75
        rect_height = 100
        rect_x = int(self.width * 0.5)- rect_width // 2
        rect_y = int(self.height * 0.55)- rect_height // 2
        #Calculate the location of decrease button
        decrease_button_center = (rect_x + rect_width + 50, rect_y + rect_height)
        if ((mouse_x - decrease_button_center[0]) ** 2 + (mouse_y - decrease_button_center[1]) ** 2) ** 0.5 <= 30:
            # Increments ship_count
            self.ship_count = (self.ship_count - 1 if self.ship_count > 1 else 5)
            # Redraw to show updated choice
            self.draw_ship_nums()

            # Update the display
            pygame.display.update()

    def erase(self):
        """Clears whatever is drawn on the page"""
        self.window.fill(self.bgcolor)

        # Update the display
        pygame.display.update()
   
