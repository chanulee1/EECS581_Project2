"""
main.py
Authors:
    - Zachary Craig
Date: 9/19/2024

Purpose: driver file for the battleship game
Inputs: N/A (-- could add command line args if we wanted to have a headless version)
"""

from UI.UIDriver import *
from GameState.GameState import *
from Logger.Logger import *
from time import sleep
import random

def main():
    # clear all logs
    clear_log()
    # create the UI object
    ui = UIDriver()
    # create the game state object
    gs = GameState()

    ## NUMBER OF SHIPS ##
    ui.draw_main_menu()
    # draw the ship number selector
    ui.draw_ship_nums()
    
    # draw ai selector
    ui.draw_ai_selector()

    # draw the go button
    ui.draw_go()

    # spin until the "GO" button is pressed
    ui.wait_for_go(ship_num_menu = True)

    ## SHIP PLACEMENTS ##
    def place_ships(player):
        # start by erasing the UI and redrawing GO button
        ui.erase()
        # then draw the transition screen for each player
        font = pygame.font.SysFont('Arial', 36)
        ui.do_text_screen(f"Player {player}'s Turn")
        
        #Loop to keep trying to place ships until they are all successfully placed
        while True:
            ships = ui.draw_ship_box(player_number = player) # <-- this includes a wait_for_go kind of call
            # store their ship placements
            #ships = ui.get_ship_placements()
            #ships = [((1, 'A'), (1, 'A')), ((2, 'A'), (2, 'B')), ((3, 'C'), (3, 'A'))] #hardcoded - REMOVE
            #Iterates through each ship and calls add_ship for player 1
            for ship in ships:
                #Try-Except block to handle errors raised in add_ship by forcing player 1 to re-place ships
                try:
                    #adds each ship to gamestate
                    gs.add_ship(ship[0], ship[1])
                    #Create flag and set it to false
                    error_occurred = False
                except (ValueError, IndexError):
                    #Tells the player what to do
                    ui.do_text_screen(f"Player {player}, please try again")
                    #Set error flag to True
                    error_occurred = True
                    #Exit the for loop to restart the while loop
                    break

            #Exit the while loop if no errors occurred
            if not error_occurred:
                break
    
    ## AI SHIP PLACEMENTS ##
    def place_ai_ships():
        # start by erasing the UI and redrawing GO button
        ui.erase()
        # then draw the transition screen for each player
        font = pygame.font.SysFont('Arial', 36)
        ui.do_text_screen(f"AI is Placing Ships")
        
        #Loop to keep trying to place ships until they are all successfully placed
        while True:
            ships_to_place = ui.get_ship_count()

            for ship in range(ships_to_place):
                random.seed()
                row_random = random.randint(1, 10 - ship)
                columns = "ABCDEFGHIJ"
                columns = columns[:10 - ship]
                col_random = random.choice("ABCDEFGHIJ")
                orientation_random = random.choice(['H', 'V'])
                ship_start = (row_random, col_random)
                ship_end = list()
                if orientation_random == 'H':
                    ship_end = (row_random, chr(ord(col_random) + ship))
                else:
                    ship_end = (row_random + ship, col_random)
                
                try:
                    gs.add_ship(ship_start, ship_end)
                    error_occurred = False
                except (ValueError, IndexError):
                    log("AI ship placement failed")
                    error_occurred = True
                    break
                
                
            #Exit the while loop if no errors occurred
            if not error_occurred:
                log("AI ships placed")
                break
    
    gs.set_difficulty(ui.get_difficulty())

    place_ships(1)

    # only place the second player's ships if it's a PvP game
    if gs.get_difficulty() == 'PvP':
        gs.turn = 2
        place_ships(2)
        gs.turn = 1

        ## MAIN LOOP ##
        # draw the large "GAME START" text
        ui.do_text_screen("GAME START!")
        
        #Loop while gameover flag is False
        gameover = False
        while not gameover:
            #ask the players to switch who is playing
            ui.do_text_screen(f"Player {gs.turn}'s Turn")
            #saves the coordinates the user shot at
            shot = ui.wait_for_shot(gs)
            result = gs.fire(shot) #shoot your shot baby
            #set flag to True and end loop
            if result =='gameover':
                gameover = True
            #return result - either "Hit!" "Miss!" or sunk
            else:
                if 'sunk' in result:
                    message = f'You Sunk Enemy Ship {result[-1]}'
                else:
                    message = result.capitalize() + '!'
                ui.do_text_screen(message)

    # if it's not a PvP game, then the AI will play
    else:
        # hit locations are only for if the AI hits a ship
        ai_hit_locations = list()
        
        # Initialized variable to store the AI's turn attack location
        ai_attack_location = list()
        
        gs.turn = 2
        place_ai_ships()
        gs.turn = 1
        
        # draw the large "GAME START" text
        ui.do_text_screen("GAME START!")
        
        #Loop while gameover flag is False
        gameover = False
        ## MAIN LOOP ##

        # Test to see if the AI ships are placed correctly, also so player can see where the AI ships are for testing purposes
        # print_ai_ships(gs)

        while not gameover:
            if gs.turn == 1:
                #ask the players to switch who is playing
                ui.do_text_screen(f"Player {gs.turn}'s Turn")#saves the coordinates the user shot at
                shot = ui.wait_for_shot(gs)
                result = gs.fire(shot) #shoot your shot baby
                #set flag to True and end loop
            else:
                ui.do_text_screen("AI's Turn")
                
                # attempts to attack until a valid attack is made
                while True:
                    try:
                        ai_attack_location = (ai_easy() if gs.get_difficulty() == 'Easy' else ai_medium(ai_hit_locations) if gs.get_difficulty() == 'Medium' else ai_hard(gs))
                        result = gs.fire(ai_attack_location)
                    except (ValueError, IndexError):
                        continue
                    break
                
            
            if result =='gameover':
                gameover = True
            #return result - either "Hit!" "Miss!" or sunk
            else:
                # If turn is 2 then use player 1 branch because gs.fire() switches the turn
                if gs.get_turn() == 2:
                    if 'sunk' in result:
                        message = f'You Sunk Enemy Ship {result[-1]}'
                    else:
                        message = result.capitalize() + '!'
                else:
                    if 'sunk' in result:
                        message = f'AI Sunk Your Ship {result[-1]}'
                        ai_hit_locations.append(ai_attack_location)
                    else:
                        message = result.capitalize() + '!'
                ui.do_text_screen(message)
    
   

    #Gameover screen
    ui.draw_gameover(gs)
    sleep(2)

    #Close the window
    pygame.quit()


### AI functions ###

# Function for AI to attack if difficulty is Easy
def ai_easy():
    shot_location = list()
    
    random.seed()
    row_random = random.randint(1, 10)
    col_random = random.choice('ABCDEFGHIJ')
    
    shot_location.append(row_random)
    shot_location.append(col_random)
    
    return shot_location

# Function for AI to attack if difficulty is Medium
def ai_medium(hit_locations):
    shot_location = list()
    
    # NEED TO IMPLEMENT
    # Should attack randomly until it hits a ship, then attack each adjacent square until the ship is sunk
    
    return shot_location

# Function for AI to attack if difficulty is Hard
def ai_hard(gs):
    # Knows where all player ships are and attacks based on that

    shot_location = list() # create an empty list to store the locations where the AI will shoot

    enemy_board = gs.player_one_board # access the player one board so the AI can see where the players ships are

    for row in range(1, 11): # Loop through all the rows
        for col in 'ABCDEFGHIJ': # Loop through all the columns
            if enemy_board.loc[row, col] in ['1', '2', '3', '4', '5']: # check if the location contains a ship, ships are represented by numbers 1-5
                shot_location.append(row) # append the row to the shot_location list
                shot_location.append(col) # append the column to the shot_location list
                return shot_location # return the shot_location list
            
# Function to print the AI's ship positions for testing purposes
def print_ai_ships(gs):
    
    ai_board = gs.player_two_board # access the AI board so we can print the AI's ship positions
    
    print("AI Ship Positions:")
    
    # Loop through each row and column to find ships
    for row in range(1, 11):
        for col in 'ABCDEFGHIJ':
            if ai_board.loc[row, col] in ['1', '2', '3', '4', '5']:
                print(f"Ship found at: ({row}, '{col}')")


if __name__ == "__main__":
    main()