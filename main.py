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
    
    gs.set_difficulty(ui.get_difficulty())

    place_ships(1)
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

    #Gameover screen
    ui.draw_gameover()
    sleep(2)

    #Close the window
    pygame.quit()


if __name__ == "__main__":
    main()