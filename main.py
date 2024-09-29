"""
main.py
Authors:
    - Zachary Craig
    - Carson Treece
    - Connor Schroeder
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

    # draw color scheme selector
    ui.draw_color_selector()

    # draw the go button
    ui.draw_go()

    # spin until the "GO" button is pressed
    ui.wait_for_go(ship_num_menu=True)

    # set the background color for the game
    ui.bgset()

    ## SHIP PLACEMENTS ##
    def place_ships(player):
        # start by erasing the UI and redrawing GO button
        ui.erase()
        # then draw the transition screen for each player
        font = pygame.font.SysFont('Arial', 36)
        ui.do_text_screen(f"Player {player}'s Turn")
        
        # Loop to keep trying to place ships until they are all successfully placed
        while True:
            ships = ui.draw_ship_box(player_number=player)
            # Iterates through each ship and calls add_ship for player 1 or 2
            for ship in ships:
                try:
                    gs.add_ship(ship[0], ship[1])
                    error_occurred = False
                except (ValueError, IndexError):
                    ui.do_text_screen(f"Player {player}, please try again")
                    error_occurred = True
                    break

            if not error_occurred:
                break
    
    ## AI SHIP PLACEMENTS ##
    def place_ai_ships():
        # start by erasing the UI and redrawing GO button
        ui.erase()
        # then draw the transition screen for each player
        font = pygame.font.SysFont('Arial', 36)
        ui.do_text_screen(f"AI is Placing Ships")
        
        # Loop to keep trying to place ships until they are all successfully placed
        while True:
            ships_to_place = ui.get_ship_count()
            gs.reset_ai_board()

            for ship in range(ships_to_place):
                random.seed()
                row_random = random.randint(1, 10 - ship)
                col_random = random.choice("ABCDEFGHIJ")
                orientation_random = random.choice(['H', 'V'])
                ship_start = (row_random, col_random)

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
        
        # Loop while gameover flag is False
        gameover = False
        while not gameover:
            if gs.turn == 1:
                # Player's turn
                ui.do_text_screen(f"Player {gs.turn}'s Turn")
                # saves the coordinates the user shot at
                shot = ui.wait_for_shot(gs)
                # shoot your shot baby
                result = gs.fire(shot)

                # set flag to True and end loop
                if result == 'gameover':
                    gameover = True
                else:
                    if 'sunk' in result:
                        message = f'You Sunk Enemy Ship {result[-1]}'
                        ui.do_text_screen(message)
                        # Player gets another turn after sinking a ship, so continue the loop without switching turns
                        continue
                    else:
                        message = result.capitalize() + '!'
                        ui.do_text_screen(message)
                        # Switch to player 2 after a hit or miss
                        gs.turn = 2
            else:
                # Player 2's turn (PvP)
                ui.do_text_screen(f"Player {gs.turn}'s Turn")
                shot = ui.wait_for_shot(gs)
                result = gs.fire(shot)

                if result == 'gameover':
                    gameover = True
                else:
                    if 'sunk' in result:
                        message = f'You Sunk Enemy Ship {result[-1]}'
                        ui.do_text_screen(message)
                        # Player 2 gets another turn after sinking a ship, so continue
                        continue
                    else:
                        message = result.capitalize() + '!'
                        ui.do_text_screen(message)
                        # Switch to player 1 after a hit or miss
                        gs.turn = 1

    # if it's not a PvP game, then the AI will play
    else:
        gs.turn = 2
        place_ai_ships()
        gs.turn = 1
        
        # draw the large "GAME START" text
        ui.do_text_screen("GAME START!")
        
        # Loop while gameover flag is False
        gameover = False
        while not gameover:
            if gs.turn == 1:
                # Player's turn against AI
                ui.do_text_screen(f"Player {gs.turn}'s Turn")
                shot = ui.wait_for_shot(gs)
                result = gs.fire(shot)

                if result == 'gameover':
                    gameover = True
                else:
                    if 'sunk' in result:
                        message = f'You Sunk Enemy Ship {result[-1]}'
                        ui.do_text_screen(message)
                        # Player gets another turn after sinking a ship, so continue
                        continue
                    else:
                        message = result.capitalize() + '!'
                        ui.do_text_screen(message)
                        # Switch to AI's turn after hit or miss
                        gs.turn = 2

            else:
                # AI's turn
                ui.do_text_screen("AI's Turn")
                
                # AI keeps trying to attack until a valid shot is made
                while True:
                    try:
                        ai_attack_location = (ai_easy() if gs.get_difficulty() == 'Easy' else ai_medium(gs) if gs.get_difficulty() == 'Medium' else ai_hard(gs))
                        result = gs.fire(ai_attack_location)
                    except (ValueError, IndexError):
                        continue
                    break

                if result == 'gameover':
                    gameover = True
                else:
                    if 'sunk' in result:
                        message = f'AI Sunk Your Ship {result[-1]}'
                        ui.do_text_screen(message)
                        # AI gets another turn after sinking a ship, so continue
                        continue
                    else:
                        message = result.capitalize() + '!'
                        ui.do_text_screen(message)
                        # Switch back to player's turn after hit or miss
                        gs.turn = 1

    # Gameover screen
    ui.draw_gameover(gs)
    sleep(2)

    # Close the window
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
def ai_medium(gs: GameState) -> tuple[int, str]:
    # Should attack randomly until it hits a ship, then attack each adjacent square until the ship is sunk
    
    attack_board = gs.enemy_board()

    cols = 'ABCDEFGHIJ\0' # cols is for easy traversal of the columns of the board via cols[ col + or - i ]
    for row in range(1, 11): # Loop through all the rows
        for col in range(len(cols)-1): # Loop through all the columns
            if len(attack_board.loc[row, cols[col]]) == 2: # if location [row, cols[col]] has been hit

                # attack_direction is the location to be shot
                # direction is if the known orientation of the ship is in that direction
                attack_up, attack_down, attack_left,attack_right = [-1, ""], [-1, ""], [-1, ""], [-1, ""]
                up, down, left, right = False, False, False, False

                #check up
                for i in range(1, 5): # 5 is the size of the biggest ship
                    try:
                        if i > 1: # mark up as a known direction of the ship
                            up = True
                        if not (attack_board.loc[row-i, cols[col]] == 'M' or len(attack_board.loc[row-i, cols[col]]) == 2): # If we haven't sent a shot up
                            attack_up = [row-i, cols[col]] # set the attack location
                            if up: # we don't want to prematurely attack if we don't know if we don't know the orientation of the ship
                                return attack_up # return attack position
                            break
                        if not len(attack_board.loc[row-i, cols[col]]) == 2: # if the spot up was a miss stop checking
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
                            if down: # we don't want to prematurely attack if we don't know if we don't know the orientation of the ship
                                return attack_down # return attack position
                            break
                        if not len(attack_board.loc[row+i, cols[col]]) == 2: # if the spot down was a miss stop checking
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
                            if left: # we don't want to prematurely attack if we don't know if we don't know the orientation of the ship
                                return attack_left # return attack position
                            break
                        if not len(attack_board.loc[row, cols[col-i]]) == 2: # if the spot left was a miss stop checking
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
                            if right: # we don't want to prematurely attack if we don't know if we don't know the orientation of the ship
                                return attack_right # return attack position
                            break
                        if attack_board.loc[row, cols[col+i]] == 'M': # if the spot right was a miss stop checking
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

                # Theoretically if one direction in known (and doesn't have a unshot spot in that direction (which is implied)) 
                # and the other direction has a spot to be shot we should shoot the other way
                if up:
                    if go_down:
                        return attack_down
                if down:
                    if go_up:
                        return attack_up
                if left:
                    if go_right:
                        return attack_right
                if right:
                    if go_left:
                        return attack_left

                # if no direction is known go in a valid direction
                if not (up or down or left or right):
                    if go_up:
                        return attack_up
                    if go_down:
                        return attack_down
                    if go_left:
                        return attack_left
                    if go_right:
                        return attack_right
                
                # if nothing has triggered this ship is sunk and move on to the next hit position

            else: # The spot was not a hit
                pass

    # If we reach here there was no hit ships that are not sunk
    random.seed()
    row_random = random.randint(1, 10)
    col_random = random.choice(cols)
    
    shot_location = list()
    shot_location.append(row_random)
    shot_location.append(col_random)
    
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