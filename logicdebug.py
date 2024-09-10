"""
main.py
Authors:
    - Michael Stang
Date: 9/5/2024

Purpose: command line based interface for testing game logic before UI is fully implemented
Inputs: User input while running via "input"
"""

from GameState.GameState import *

def main():
    """Quick debug program to allow placing ships and firing in game logic to ensure validity of internal game systems
    """
    game = GameState()
    while True:
        print("PLAYER 1 BOARD\n")
        print(game.player_one_board)
        print("\nPLAYER 2 BOARD\n")
        print(game.player_two_board)
        command = input(">> ")
        command_break = command.split()

        try:
            match command_break[0]:
                case "quit":
                    break
                
                case "place": # place PLAYER_NUM START_LETTER START_NUM END_LETTER END NUM
                    game.turn = int(command_break[1])
                    game.add_ship((int(command_break[3]), command_break[2]), (int(command_break[5]), command_break[4]))
                
                case "fire":
                    game.turn = int(command_break[1])
                    game.fire((int(command_break[3]), command_break[2]))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()