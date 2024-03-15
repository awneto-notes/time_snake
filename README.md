### The timed Snake game

This is a simple implementation of the classic "Snake" game with an additional _twist_.
The game features a snake that moves on a square grid. However, instead of eating to grow larger, it will eat to reduce its length, which increases as time passes.
This script was written with significant contributions from GPT 3.5.

Below are the main components and functionalities of the code:

### GameWindow Class:
Manages the game window, including screen configuration, filling the background, drawing the gridline and handling events.
### Cobra Class:
Represents the snake in the game, dealing with changes in movement, growth and orientation.
### Main Cycle:
Controls the game's core logic, updating the screen, handling player input, and managing the snake's movement and growth.
### Constants:
Defines grid size, colors, screen dimensions, and other game-related constants.

### How to play:
- Use the arrow keys to control the snake's movement.
- The length of the snake will increase as time passes.
- Eat to reduce the snake's length.
- Stay clear from the walls and the snake's body.
- The snake's head jumps to the other side of the screen if it goes out of bounds.

🐍🎮
