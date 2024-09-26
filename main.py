"""
main.py
Authors:
    - Zachary Craig
    - Carson Treece
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
                        ai_attack_location = (ai_easy() if gs.get_difficulty() == 'Easy' else ai_medium(gs, ai_hit_locations) if gs.get_difficulty() == 'Medium' else ai_hard(gs))
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
def ai_medium(gs: GameState, hit_locations) -> tuple[int, str]:
    # Should attack randomly until it hits a ship, then attack each adjacent square until the ship is sunk
    
    # NEED TO IMPLEMENT

    known_attack, shot_location = known_location(gs)

    if not known_attack:
        random.seed()
        row_random = random.randint(1, 10)
        col_random = random.choice('ABCDEFGHIJ\0')
        
        shot_location.append(row_random)
        shot_location.append(col_random)
    else:
        print(f'shot_location = {shot_location}')
    
    return shot_location

# Determines if there's a know location of a ship
def known_location(gs: GameState) -> tuple[bool, list[int, str]]:

    # So I need to determine if there's a know location based on gs.enemy_board()
    # a '*' means that the it was a hit, 'M' is a miss, '~' is not shot yet, 1-5 means that a ship is there
    # I believe those are the only symbols on a player board

    attack_board = gs.enemy_board()

    cols = 'ABCDEFGHIJ'
    for row in range(1, 11): # Loop through all the rows
        for col in range(len(cols)): # Loop through all the columns
            # print(f'[{row}, {cols[col]}] = {attack_board.loc[row, cols[col]]}')
            if len(attack_board.loc[row, cols[col]]) == 2:
                # print("Entered the hit if")

                attack_up = [-1, ""]
                attack_down = [-1, ""]
                attack_left = [-1, ""]
                attack_right = [-1, ""]
                up = False
                down = False
                left = False
                right = False

                #check up
                for i in range(1, 5): # 5 is the size of the biggest ship
                    try:
                        if i > 1: # mark up as a known direction of the ship
                            up = True
                        if not (attack_board.loc[row-i, cols[col]] == 'M' or len(attack_board.loc[row-i, cols[col]]) == 2): # If we haven't sent a shot up
                            attack_up = [row-i, cols[col]]
                            # print(f'Setting attack_up as = {attack_up}')
                            if i > 1: # we don't want to prematurely attack up if we know it's to the side or below
                                return (up, attack_up)
                            break
                        if not len(attack_board.loc[row-i, cols[col]]) == 2: # if the spot up was not a hit
                            break
                    except: # only errors when it hits the edge of the board
                        break
                # check down
                for i in range(1, 5): # 5 is the size of the biggest ship
                    try:
                        if i > 1: # mark down as a known direction of the ship
                            down = True
                        if not (attack_board.loc[row+i, cols[col]] == 'M' or len(attack_board.loc[row+i, cols[col]]) == 2): # If we haven't sent a shot down
                            attack_down = [row+i, cols[col]]
                            # print(f'Setting attack_down as {attack_down}')
                            if i > 1: # we don't want to prematurely attack down if we know it's to the side
                                return (down, attack_down)
                            break
                        if not len(attack_board.loc[row+i, cols[col]]) == 2: # if the spot down was not a hit
                            break
                    except: # only errors when it hits the edge of the board
                        break
                pass
                # check left
                for i in range(1, 5): # 5 is the size of the biggest ship
                    try:
                        if i > 1: # mark left as a known direction of the ship
                            left = True
                        if not (attack_board.loc[row, cols[col-i]] == 'M' or len(attack_board.loc[row, cols[col-i]]) == 2): # If we haven't sent a shot left
                            attack_left = [row, cols[col-i]]
                            # print(f'Setting attack_left as {attack_left}')
                            if i > 1: # we don't want to prematurely attack left if we know it's to the right
                                return (left, attack_left)
                            break
                        if not len(attack_board.loc[row, cols[col-i]]) == 2: # if the spot left was not a hit
                            break
                    except: # only errors when it hits the edge of the board
                        break
                # check right
                for i in range(1, 5): # 5 is the size of the biggest ship
                    try:
                        if i > 1: # mark right as a known direction of the ship
                            right = True
                        if not (attack_board.loc[row, cols[col+i]] == 'M' or len(attack_board.loc[row, cols[col+i]]) == 2): # If we haven't sent a shot right
                            attack_right = [row, cols[col+i]]
                            # print(f'Setting attack_right as {attack_right}')
                            if i > 1: # this if statement is here to keep the structure the same
                                return (right, attack_right)
                            break
                        if attack_board.loc[row, cols[col+i]] == 'M': # if the spot right was a miss stop checking right
                            break
                    except: # only errors when it hits the edge of the board
                        break
                # Checked all directions and the ship has no unshot spots in a known direction
                # Now I need to check what directions we can and should shoot

                # marking which directions have spots to shoot
                go_up = True
                go_down = True
                go_left = True
                go_right = True
                if attack_up == [-1, ""]:
                    go_up = False
                if attack_down == [-1, ""]:
                    go_down = False
                if attack_left == [-1, ""]:
                    go_left = False
                if attack_right == [-1, ""]:
                    go_right = False

                print(f'[{row}, {cols[col]}]')
                print(f'up = {up}\t\tdown = {down}\t\tleft = {left}\t\tright = {right}')
                print(f'go_up = {go_up}\t\tgo_down = {go_down}\t\tgo_left = {go_left}\t\tgo_right = {go_right}')
                print(f'attack_up = {attack_up}\tattack_down = {attack_down}\tattack_left = {attack_left}\tattack_right = {attack_right}')

                # Theoretically if one direction in known (and doesn't have a unshot spot in that direction which is implied) 
                # and the other direction has a spot to be shot we should shoot the other way
                if up:
                    if go_down:
                        return (True, attack_down)
                if down:
                    if go_up:
                        return (True, attack_up)
                if left:
                    if go_right:
                        return (True, attack_right)
                if right:
                    if go_left:
                        return (True, attack_left)
                
                # if no direction is known go in a valid direction
                if not (up or down or left or right):
                    # print("no known direction")
                    if go_up:
                        return (True, attack_up)
                    if go_down:
                        return (True, attack_down)
                    if go_left:
                        return (True, attack_left)
                    if go_right:
                        return (True, attack_right)
                
                # if nothing has triggered this ship is sunk and move on to the next hit position
                        
            else: # The spot was not a hit
                pass
    # If we reach here there was no hit ships that were not sunk
    return (False, [])
                


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