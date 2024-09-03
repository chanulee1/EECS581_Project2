"""
GameState.py
Authors:
    - Michael Stang
    - First Last
Date: 9/2/2024

Purpose: does the backend driving of the battle ship game state
"""
from Logger.Logger import *
import pandas

def create_blank_board():
    """Utility function to help with game creation
    Will create and return a blank 10x10 board filled with '~'s.
    The rows are denoted by the numbers 1-10 and columns denoted by the letters A-J
    The entire data structure is represented using a DataFrame from the Pandas library
    @return DataFrame: Returns a DataFrame that represents the board, it is filled with ~s.
    """
    
    # A variable to hold the '~'s that will make up the internals of our DataFrame
    data = [] 
    
    # Fills the data list with 10 lists of 10 '~'s

    # Loops 10 times to create the lists
    for _ in range(10): 
        # Actually adds the lists to the initial data list
        data.append([]) 
        # Loops 10 times within each list (row)
        for _ in range(10): 
             # Adds a ~ for each element
            data[-1].append('~')

    # ^ this could be a list comprehension to reduce lines, but I feel nested comprehensions are a pain to read

    # Creates the DataFrame as specified by the Pandas library with the data we created above and the row and column names
    blank_board = pandas.DataFrame(data, index=list(range(1,11)), columns=['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])

    # Returns the board we created
    return blank_board


def verify_coord(coord):
    """Error checking utility function that takes in a coordinate and verifies that it is a board position
    It is valid if it's Int is between 1 and 10 (inclusive) and its String is in between 'A'-'J' (inclusive)
    coord[0] = Int/Row
    coord[1] = String/Column
    This is slightly backwards from the usual order the elements are said in Battleship, but I'm sticking with it this way to match Panda's conventions
    @param (int, string) coord: Given a tuple with an int representing the row and a string representing the column
    @return Bool: Returns True if it is a valid position and False if it is not
    """

    # Simple one line condition check. This doesn't NEED to be a function, but it makes the code much more readable and allows for easy additional error checking if needed later.
    return ((coord[0] >= 1 and coord[0] <= 10) and (coord[1] in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']))


class GameState:
    def __init__(self):
        log("I'm in GameState!")

        # Panda DataFrame representing the board for Player 1
        self.player_one_board = create_blank_board()

        # Panda DataFrame representing the board for Player 2
        self.player_two_board = create_blank_board()

        # Int to keep track of whose turn it is. 1 = Player 1's turn, 2 = Player 2's turn.
        self.turn = 1

        # Internal tracking int to track how many ship spaces player one has remaining
        self._player_one_ships = 0
        
        # Internal tracking int to track how many ship spaces player two has remaining
        self._player_two_ships = 0

        #print(self.player_one_board.loc[2, 'A'])

    def fire(self, coord):
        """Main method used to calculate the results of each player firing at a given coord
        Both returns a string to easily tell what happened and updates gamestate
        @param (int, string) coord: The coords are a mix of an int and a string and represent the space the active player is shooting at
        @return string: Returns a string representing the action that happened (and updates gamestate). "miss" "hit" "gameover" "sunk #" are all possible outputs.
        """
        # returns a string "hit", "miss", "gameover"
        # updates game board (p1/p2's) accordingly
        
        # ERROR CHECKING SECTION

        # Checks if the coords provided are not in the 10x10
        if not verify_coord(coord):
            # Logs the error in coordinate passing using the Logger.py
            log(f"fire(self, coord): fire was passed an invalid coordinate ({coord}) that is not in the 10x10 board.")
            # Raises an IndexError to be handled
            raise IndexError(f"fire(self, coord): fire was passed an invalid coordinate ({coord}) that is not in the 10x10 board.")

        # CALCULATE RESULT SECTION

        # Checks whose turn it is
        if self.turn == 1:
            # If it's player 1's turn, then player two's board is the "opponent's board"
            opponent_board = self.player_two_board
            # if it's player 1's turn, the ships we're tracking is the opponent's to see if player 2 may win
            opponent_ship_segments = self._player_two_ships
        else:
            # If it's player 2's turn, then player two's board is the "opponent's board"
            opponent_board = self.player_one_board
            # if it's player 2's turn, the ships we're tracking is the opponent's to see if player 1 may win
            opponent_ship_segments = self._player_one_ships

        match opponent_board.loc[coord[0], coord[1]]:
            # The target was empty water
            case "~":
                # Mark the spot with a "miss"
                opponent_board.loc[coord[0], coord[1]] = "M"

                # Swaps the turn
                self.turn = 2 if (self.turn == 1) else 1

                # Returns the "miss" status of the shot
                return "miss"

            # The target was an unhit part of a ship
            case '1' | '2' | '3' | '4' | '5':
                
                # Checks if this segement is the opponent only has this final ship segment
                if opponent_ship_segments == 1:
                    # If so, returns that the game is over
                    return "gameover"

                # Marks the spot as "hit" by adding a "*" to the end of the number
                opponent_board.loc[coord[0], coord[1]] = opponent_board.loc[coord[0], coord[1]] + "*"
                
                # Removes one ship segment from the counter
                opponent_ship_segments -= 1

                # Swaps whose turn it is
                self.turn = 2 if (self.turn == 1) else 1

                # Checks the opponent's board to see if there are any more of unhit versions of the target that was hit. 
                # This works for detecting sunk ships since there aren't multiple of the same length ships.
                if opponent_board.isin(opponent_board.loc[coord[0], coord[1]][0]).any().any():
                    
                    #Returns "hit" when the coord has a ship, but doesn't cause a sink
                    return "hit"
                
                else:

                    # Returns "sunk #" where # is the length of the ship that was sunk. Again this works well since there is only 1 ship of each length.
                    return f"sunk {opponent_board.loc[coord[0], coord[1]][0]}"
                    
            # The target was not any of those, which, assuming no issues with board creation, should be a spot already targeted previously. This shouldn't be possible.
            case _:

                # Logs the error in coordinate passing using the Logger.py
                log(f"fire(self, coord): fire was passed a coordinate ({coord}) that is in the 10x10 but should not be targeted '{opponent_board.loc[coord[0], coord[1]]}'.")
                # Raises an ValueError to be handled
                raise ValueError(f"fire(self, coord): fire was passed a coordinate ({coord}) that is in the 10x10 but should not be targeted '{opponent_board.loc[coord[0], coord[1]]}'.")


    def add_ship(self, start, end):
        """Main method used to add ships to board
        Does error checking, but does not handle it
        The ship is created between the two points.
        Uses the self.player to determine who is placing ships currently.
        @param (int, string) start: The start coordinate for the start of the ship
        @param (int, string) end: The ending coordinate for the end of the ship
        @return Bool: Returns True if the ship was created
        """
        # adds a ship between start and end
        # needs to check if the ship is a line
        # needs to increment the total of ship segments for the player that placed it

        # ERROR CHECKING SECTION
        # Error to check for: Not straight line, not within 10x10, and overlapping (this will be done later to avoid recomputing things) [maybe more than 5 in length is error, or maybe its scalability]

        # Check Straight Line
        # Checks if the two coords passed are on the same row or same column to ensure a straight line
        if not ((start[0] == end[0]) or (start[1] == end[1])): 
            log(f"add_ship(start, end): add_ship was passed two coordinates ({start} & {end}) that are not in a straight line")
            raise ValueError(f"add_ship(start, end): add_ship was passed two coordinates ({start} & {end}) that are not in a straight line")

        # Check that all values are within the 10x10
        # As long as both ends are within the 10x10, all values must be
        if not (verify_coord(start) and verify_coord(end)):
            log(f"add_ship(start, end): add_ship was passed two coordinates ({start} & {end}) that result in a ship outside of the board's bounds")
            raise IndexError(f"add_ship(start, end): add_ship was passed two coordinates ({start} & {end}) that result in a ship outside of the board's bounds")

        # Calculate Length

        # If the points are in the same row
        if start[0] == end[0]:
            
            #calculate using letters (and ASCII)
            ship_length = abs(ord(start[1]) - ord(end[1])) + 1
        
        # If the points are in the same column
        else:

            # calculate using nums (rows)
            ship_length = abs(start[0] - end[0]) + 1
            
        # Place Ship

        # Sets the "current_ship_count" var so we can edit it later to keep track of the ships out there
        if self.turn == 1:
            # Player 1 is placing ships right now
            current_ship_count = self._player_one_ships
            current_board = self.player_one_board
        else:
            # Player 2 is placing ships right now
            current_ship_count = self._player_two_ships
            current_board = self.player_two_board

        row = start[0] # Ints
        column = start[1] # Strings

        for _ in range(ship_length):
            
            # Checks to make sure we're not overlapping
            if current_board.loc[row, column] == '~':
                # Sets the position to the ship length number
                current_board.loc[row, column] = ship_length
                # Ups the current ship count
                current_ship_count += 1

            # If there is already a ship (or something else that isn't water)
            else:
                # Typical error procedure
                log(f"add_ship(start, end): add_ship was passed two coordinates ({start} & {end}) that result in overlapping ships at ({row},{column})")
                raise ValueError(f"add_ship(start, end): add_ship was passed two coordinates ({start} & {end}) that result in overlapping ships at ({row},{column})")

            # If they are the same row, then we need to increment the letters
            if start[0] == end[0]:

                # If our current column is less than the ending column
                if ord(column) < ord(end[1]):
                    column = str(ord(column) + 1)

                # If we're going backwards
                else:
                    column = str(ord(column) - 1)
            
            # If they are in the same column, then we need to increment the nums
            else:

                # If the current row is lower than the ending row we add 1
                if row < end[0]:
                    row += 1

                # If the current row is higher than the end, we're going backwards and should subtract to get to the end
                else:
                    row -= 1

        return True
