import pygame
import sys
import copy
from pygame.locals import *


class GameWindow:
    def __init__(self, width, height, caption):
        self.width = width
        self.height = height
        self.caption = caption
        self._screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        self._clock = pygame.time.Clock()
    
    def get_screen(self):
        return self._screen
    
    def fill_background(self, color):
        self._screen.fill(color)
       
    def update_display(self):
        pygame.display.flip()

    def set_fps(self, fps):
        self._clock.tick(fps)
             
    def draw_grid_lines(self, grid_size, grid_color):
        for x in range(0, self.width, grid_size):
            pygame.draw.line(self._screen, grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_size):
            pygame.draw.line(self._screen, grid_color, (0, y), (self.width, y))    
    
    def draw_snake_cells(self, snake_positions, cell_color, grid_size):
        for i, (cell_x, cell_y) in enumerate(snake_positions):
            pygame.draw.rect(self._screen, cell_color, (cell_x, cell_y, grid_size, grid_size))
   
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
              

class Snake:
    def __init__(self, initial_positions):
        self.positions = initial_positions

    def increase_size(self):
        tail_x, tail_y = self.positions[-1]
        new_tail = (tail_x - GRID_SIZE, tail_y)
        self.positions.append(new_tail)

    def decrease_size(self):
        if len(self.positions) > 1:
            self.positions.pop()

    def reset_positions(self):
        self.positions = [(100, 80), (90, 80), (80, 80), (70, 80), (60, 80), (50, 80), (40, 80), (30, 80), (20, 80), (10, 80)]

    def get_orientation(self):
        if len(self.positions) <= 1:
            return "ERROR"
            
        x0, y0 = self.positions[0]
        x1, y1 = self.positions[1]
        crossed_boundary = False
        
        dx = x1-x0
        dy = y1-y0
        
        if abs(dx) > GRID_SIZE or abs(dy) > GRID_SIZE: # if the snake has just crossed the screen boundary
            crossed_boundary = True
        
        if x0 == x1:
            if y0 >= y1:
                return("DOWN") if not(crossed_boundary) else ("UP")
            else:
                return("UP") if not(crossed_boundary) else ("DOWN")
        elif y0 == y1:
            if x0 >= x1:
                return("RIGHT") if not(crossed_boundary) else ("LEFT")
            else:
                return("LEFT") if not(crossed_boundary) else ("RIGHT")
        else:
            return "ERROR"


    def _move_head(self, direction):
        head_x, head_y = self.positions[0]
        if direction == "UP":
            self.positions[0] = (head_x, (head_y - GRID_SIZE) % game_window.height)
        elif direction == "DOWN":
            self.positions[0] = (head_x, (head_y + GRID_SIZE) % game_window.height)
        elif direction == "LEFT":
            self.positions[0] = ((head_x - GRID_SIZE) % game_window.width, head_y)
        elif direction == "RIGHT":
            self.positions[0] = ((head_x + GRID_SIZE) % game_window.width, head_y)
                   

    def _move_body(self, old_positions):
        for i in range(1, len(self.positions)):
            self.positions[i] = (old_positions[i - 1][0], old_positions[i - 1][1])


    def move(self, keys):
        old_positions = copy.deepcopy(self.positions)
        orientation = self.get_orientation()
        key_pressed = False

        if keys[K_UP] and not (keys[K_LEFT] or keys[K_RIGHT]):
            self._move_head("UP")
            key_pressed = True
        if keys[K_DOWN] and not (keys[K_LEFT] or keys[K_RIGHT]):
            self._move_head("DOWN")
            key_pressed = True
        if keys[K_LEFT] and not (keys[K_UP] or keys[K_DOWN]):
            self._move_head("LEFT")
            key_pressed = True
        if keys[K_RIGHT] and not (keys[K_UP] or keys[K_DOWN]):
            self._move_head("RIGHT")
            key_pressed = True

        if not key_pressed:
            if orientation == "UP":
                self._move_head("UP")
            elif orientation == "DOWN":
                self._move_head("DOWN")
            elif orientation == "LEFT":
                self._move_head("LEFT")
            elif orientation == "RIGHT":
                self._move_head("RIGHT")
        
        self._move_body(old_positions)


# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
GRID_COLOR = (255, 255, 255)  # White
BACKGROUND_COLOR = (0, 0, 0)  # Black
CELL_COLOR = (0, 128, 64)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Create a GameWindow object
game_window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake timer")

# Initial cell positions
initial_positions = [(100, 80), (90, 80), (80, 80), (70, 80), (60, 80), (50, 80), (40, 80), (30, 80), (20, 80), (10, 80)]

# Create a Snake object
snake = Snake(initial_positions)

# Clock and timer
clock = pygame.time.Clock()
move_timer = pygame.time.get_ticks()


# Main loop
while True:

    game_window.set_fps(10)  # Limit to 10 frames per second
    game_window.fill_background(BACKGROUND_COLOR)

    # Draw grid lines
    game_window.draw_grid_lines(GRID_SIZE, GRID_COLOR)
    
    # Draw the cells of the snake on the screen
    game_window.draw_snake_cells(snake.positions, CELL_COLOR, GRID_SIZE)

    # Handle game events
    game_window.handle_events()

    # Check if time has elapsed to increase the snake size
    if pygame.time.get_ticks() - move_timer > 100:  # 0.1 second
        move_timer = pygame.time.get_ticks()
        if len(snake.positions) > 1:
            snake.increase_size()
        else:
            snake.reset_positions()

    keys = pygame.key.get_pressed()
    snake.move(keys)
    
    game_window.update_display()
    