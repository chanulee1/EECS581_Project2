# EECS 581 Project 2

For this project, we (Team 27) enhanced Team 41's implementation of **Project 1**, the game **Battleship**. The following is a summary of the changes we made to implement the features specified by **Project 2**.

## Features

### AI Opponent

To implement this feature, we first needed to add a section to the main menu that allowed the player to choose between playing against a human or AI opponent. If the player chose to play against the AI, we needed to allow the player to choose the difficulty of the AI. 

We also needed to program each difficulty level of the AI and allow the AI to place ships and attack the player.

To do this, we modified these files:

#### `GameState.py`

- Add the AI difficulty attribute and get and set methods to the `GameState` class.
- Get methods for the player turn and boards.

#### `UIDriver.py`

- Add methods to the `UIDriver` class which grab the player-selected game mode, draw buttons and process user input.
- Draw objects and text based on game mode.

#### `main.py`

- Draw the game mode selector, set the game mode.
- Add funtion for placing AI ships (random).
- Add lists to store the AI's hit and attack locations.
- Add AI attack functions for each level of difficulty.
  - Easy: Select random row and column, and attack that location.
  - Medium: Find location that has been hit and attack adjacent squares based on orientation of the ship if known. If there are no hit and unsunk ships, attack randomly.
  - Hard: Access the player board and attack ship locations.

### Custom Addition 1: Extra Turn

For our first custom addition, we are allowing the players to take an extra turn if they sink a ship during their turn. To implement this, we modified these files:

#### `Main.py`

- Check if the player/AI whose turn it is sunk a ship, and give them an extra turn if all ships are not sunk yet.

### Custom Addition 2: Theme Selector

For our second custom addition, we are adding a section to the main menu that allows the player to select a color scheme for the game. The colors include blue, red, orange, grey, and light blue. Each theme also includes different color accents to buttons and other objects in the game. To implement this, we modified these files:

#### `UIDriver.py`

- Add color scheme options.
- Add color scheme attribute to the `UIDriver` class.
- Check inputs to the scheme selector, get the player-selected scheme.
- Draw the scheme selector on the main menu.
- Change how game objects are drawn based on the color scheme.

#### `Main.py`

- Draw the color scheme selector, set background color.