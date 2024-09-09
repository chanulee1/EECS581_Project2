"""
main.py
Authors:
    - Pierce Lane
    - Chase Horner
Date: 9/2/2024

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

    # draw the go button
    ui.draw_go()

    # spin until the "GO" button is pressed
    ui.wait_for_go(ship_num_menu = True)

    ## SHIP PLACEMENTS ##
    # start by erasing the UI and redrawing GO button
    ui.erase()
    # then draw the transition screen for p1
    ui.do_text_screen("Player 1's Turn")
    ui.draw_laptop(1)
    # draw their ship box and let them drag stuff
    ui.draw_ship_box(player_number = 2) # <-- this includes a wait_for_go kind of call
    # store their ship placements
    p1ships = ui.get_ship_placements()

    # then draw the transition screen for p2
    ui.do_text_screen("Player 2's Turn")
    # draw their ship box and let them drag stuff
    ui.draw_ship_box(player_number = 2) # <-- this includes a wait_for_go kind of call
    # store their ship placements
    p2ships = ui.get_ship_placements()

    ## MAIN LOOP ##
    # draw the large "GAME START" text
    ui.do_text_screen("GAME START!")
    gameover = False
    while not gameover:
        #ask the players to switch who is playing
        ui.do_text_screen(f"Player {gs.turn}'s Turn")
        #saves the coordinates the user shot at
        shot = ui.wait_for_shot()
        result = gs.fire(shot) #shoot your shot baby
        if result =='gameover':
            gameover = True
        else:
            ui.draw_shot_result(result)

    ui.draw_gameover()
    # play again feature?

    # close the window
    pygame.quit()

if __name__ == "__main__":
    # parse command line args here if wanted
    main()