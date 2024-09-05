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

def main_menu_loop():
    # should wait for inputs from the main menu in UIDriver
    pass

def main():
    # clear all logs
    clear_log()
    # create the UI object
    ui = UIDriver()
    # create the game state object
    gs = GameState()

    ## do main menu
    ui.draw_main_menu()
    # draw the ship number selector
    ui.draw_ship_nums()
    # draw the ship box
    ui.draw_ship_box() #Not sure what this is here for yet
    # draw the go button
    ui.draw_go()

    # spin until the "GO" button is pressed
    waiting = True
    while waiting:
        for event in pygame.event.get():
                #Quits if event type is quit
                if event.type == pygame.QUIT:
                    pygame.quit()

                #Stores the mouse position for every click to determine if a button was clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # Check if increase button is clicked, which is determined by is_button_clicked function
                    ui.up_button_clicked(mouse_x, mouse_y)
                    ui.down_button_clicked(mouse_x, mouse_y)
                    waiting = not ui.go_clicked(mouse_x, mouse_y)

    ui.erase()
    sleep(2)
    # draw player 1's laptop
    ui.draw_laptop(1)
    # wait for them to press the GO button
    ui.go_clicked()
    # get their ship placements
    p1ships = ui.get_ship_placements()

    # draw player 2's laptop
    ui.draw_laptop(2)
    # wait for them to press the GO button
    ui.go_clicked()
    # get their ship placements
    p2ships = ui.get_ship_placements()
    
    sleep(2)
    """Notes:
    - I don't immediately see a way for UI to be able to not track ship placements
        - i.e. I think UI will need to know the pandas data type"""

    # finally, tell GameState what we've found out

    # then start the main loop
    # main loop:
        # UIDriver.wait_for_shot()
        # GameState.fire()
            # check for game over here
        # UIDriver.draw() -- might need another function for drawing game over screen

    gameover = False
    while not gameover:
        #ask the players to switch who is playing
        ui.draw_switch_screen(gs.turn)
        #saves the coordinates the user shot at
        shot = ui.wait_for_shot()
        result = gs.shoot(shot) #shoot your shot baby
        if result =='gameover':
            gameover = True
        else:
            ui.draw_shot_result(result)

    ui.draw_gameover()
    # play again feature?

    # close the window
    pygame.quit()
    pass

if __name__ == "__main__":
    # parse command line args here if wanted
    main()