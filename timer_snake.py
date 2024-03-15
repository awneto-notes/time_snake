import pygame
import sys
import copy
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
GRID_COLOR = (255, 255, 255)  # White
BACKGROUND_COLOR = (0, 0, 0)  # Black
CELL_COLOR = (0, 128, 64) 

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake timer")

# Initial cell positions
cell_positions = [(100, 80), (90, 80), (80, 80), (70, 80), (60, 80), (50, 80), (40, 80), (30, 80), (20, 80), (10, 80)]


clock = pygame.time.Clock()
move_timer = pygame.time.get_ticks()


    


def increase_snake_size(cell_positions):
    tail_x, tail_y = cell_positions[-1]
    new_tail = (tail_x - GRID_SIZE, tail_y)
    cell_positions.append(new_tail)
    return(cell_positions)
    
def get_snake_orientation(cell_positions):
    if (cell_positions[0][0] == cell_positions[1][0]):  # if the head of the snake is parallel to the horizontal axis
        if (cell_positions[0][1] >= cell_positions[1][1]): # if the snake is moving down
            return("DOWN")
        else:                                              # if the snake is moving up
            return("UP")
    elif (cell_positions[0][1] == cell_positions[1][1]):    # if the head of the snake is parallel to the vertical axis
        if (cell_positions[0][0] >= cell_positions[1][0]): # if the snake is moving right
            return("RIGHT")
        else:                                              # if the snake is moving left
            return("LEFT")
    else:
        return("ERROR")
            
def move_snake_head(cell_positions, direction):
    if direction == "UP":
        cell_positions[0] = (cell_positions[0][0], cell_positions[0][1] - GRID_SIZE)
    elif direction == "DOWN":
        cell_positions[0] = (cell_positions[0][0], cell_positions[0][1] + GRID_SIZE)
    elif direction == "LEFT":
        cell_positions[0] = (cell_positions[0][0] - GRID_SIZE, cell_positions[0][1])
    elif direction == "RIGHT":
        cell_positions[0] = (cell_positions[0][0] + GRID_SIZE, cell_positions[0][1])
        
    return(cell_positions)
    
    
def move_snake_body(cell_positions, old_positions):
    for i in range(1,len(cell_positions)):
        cell_positions[i] = (old_positions[i - 1][0], old_positions[i - 1][1])   
    return(cell_positions)
        
  
def move_snake(keys, cell_positions):
    old_positions = copy.deepcopy(cell_positions)
    orientation = get_snake_orientation(cell_positions)
    key_pressed = False
    
    if keys[K_UP] and not (keys[K_LEFT] or keys[K_RIGHT]):  # UP
        cell_positions = move_snake_head(cell_positions, "UP")
        key_pressed = True
        
    if keys[K_DOWN] and not (keys[K_LEFT] or keys[K_RIGHT]):    #DOWN
        cell_positions = move_snake_head(cell_positions, "DOWN")
        key_pressed = True
        
    if keys[K_LEFT] and not (keys[K_UP] or keys[K_DOWN]):   # LEFT
        cell_positions = move_snake_head(cell_positions, "LEFT")
        key_pressed = True
        
    if keys[K_RIGHT] and not (keys[K_UP] or keys[K_DOWN]):  # RIGHT
        cell_positions = move_snake_head(cell_positions, "RIGHT")
        key_pressed = True
        
    if not key_pressed:
        if orientation == "UP":
            cell_positions = move_snake_head(cell_positions, "UP")
        elif orientation == "DOWN":
            cell_positions = move_snake_head(cell_positions, "DOWN")
        elif orientation == "LEFT":
            cell_positions = move_snake_head(cell_positions, "LEFT")
        elif orientation == "RIGHT":
            cell_positions = move_snake_head(cell_positions, "RIGHT")
            
    cell_positions = move_snake_body(cell_positions, old_positions)
    return(cell_positions)

# Main loop
while True:
    screen.fill(BACKGROUND_COLOR)

    # Draw grid lines
    for x in range(0, screen_width, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
    for y in range(0, screen_height, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))

    # Draw the cells
    for i, (cell_x, cell_y) in enumerate(cell_positions):
        pygame.draw.rect(screen, CELL_COLOR, (cell_x, cell_y, GRID_SIZE, GRID_SIZE))


    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    cell_positions = move_snake(keys, cell_positions)
    
    # Check if 2 seconds have elapsed to add a new cell
    if pygame.time.get_ticks() - move_timer > 2000:  # 2 seconds
        move_timer = pygame.time.get_ticks()
        cell_positions = increase_snake_size(cell_positions)

    pygame.time.delay(1)
    pygame.display.flip()
    clock.tick(10)  # Limit to 60 frames per second
    
    
    
    
    
'''
def move_snake_keys(keys, cell_positions):
    key_pressed = False
    old_positions = copy.deepcopy(cell_positions)
    if keys[K_UP] and not (keys[K_LEFT] or keys[K_RIGHT]):  # UP
        cell_positions[0] = (cell_positions[0][0], cell_positions[0][1] - GRID_SIZE)
        key_pressed = True
    if keys[K_DOWN] and not (keys[K_LEFT] or keys[K_RIGHT]):    #DOWN
        cell_positions[0] = (cell_positions[0][0], cell_positions[0][1] + GRID_SIZE)
        key_pressed = True
    if keys[K_LEFT] and not (keys[K_UP] or keys[K_DOWN]):   # LEFT
        cell_positions[0] = (cell_positions[0][0] - GRID_SIZE, cell_positions[0][1])
        key_pressed = True
    if keys[K_RIGHT] and not (keys[K_UP] or keys[K_DOWN]):  # RIGHT
        cell_positions[0] = (cell_positions[0][0] + GRID_SIZE, cell_positions[0][1])
        key_pressed = True
        
        
        
    # Update positions of subsequent cells
    if key_pressed:
        for i in range(1,len(cell_positions)):
            cell_positions[i] = (old_positions[i - 1][0], old_positions[i - 1][1])    
     
    return(cell_positions)
'''