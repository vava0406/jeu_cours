"""
Snake Eater
Made with PyGame
"""
import pygame
import sys
import time
import random
from typing import List, Tuple


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
FRAME_SIZE_X = 720
FRAME_SIZE_Y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))


# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
HEIGHT_WIDTH: int = 10
POSITION_X: int = HEIGHT_WIDTH * 10
POSITION_Y: int = HEIGHT_WIDTH * 5

snake_pos: List[int] = [POSITION_X, POSITION_Y]
snake_body: List[List[int]] = [
    [POSITION_X, POSITION_Y],
    [POSITION_X - HEIGHT_WIDTH, POSITION_Y],
    [POSITION_X - (2 * HEIGHT_WIDTH), POSITION_Y],
]

food_pos: List[int] = [
    random.randrange(1, (FRAME_SIZE_X // HEIGHT_WIDTH)) * HEIGHT_WIDTH,
    random.randrange(1, (FRAME_SIZE_Y // HEIGHT_WIDTH)) * HEIGHT_WIDTH,
]
food_spawn: bool = True

direction: str = 'RIGHT'
change_to: str = direction

score: int = 0


# Game Over
font_height: int = 90

def game_over() -> None:
    my_font: pygame.font.Font = pygame.font.SysFont('times new roman', font_height)
    game_over_surface: pygame.Surface = my_font.render('YOU DIED', True, RED)
    game_over_rect: pygame.Rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X / 2, FRAME_SIZE_Y / 4)
    game_window.fill(BLACK)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, RED, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X/HEIGHT_WIDTH, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= HEIGHT_WIDTH
    if direction == 'DOWN':
        snake_pos[1] += HEIGHT_WIDTH
    if direction == 'LEFT':
        snake_pos[0] -= HEIGHT_WIDTH
    if direction == 'RIGHT':
        snake_pos[0] += HEIGHT_WIDTH

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [
            random.randrange(1, (FRAME_SIZE_X // HEIGHT_WIDTH)) * HEIGHT_WIDTH,
            random.randrange(1, (FRAME_SIZE_Y // HEIGHT_WIDTH)) * HEIGHT_WIDTH,
        ]
    food_spawn = True

    # GFX
    game_window.fill(BLACK)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(
            game_window, GREEN, pygame.Rect(pos[0], pos[1], HEIGHT_WIDTH, HEIGHT_WIDTH)
        )

    # Snake food
    pygame.draw.rect(game_window, WHITE, 
                    pygame.Rect(food_pos[0], 
                    food_pos[1], HEIGHT_WIDTH, HEIGHT_WIDTH))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > FRAME_SIZE_X-HEIGHT_WIDTH:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > FRAME_SIZE_Y-HEIGHT_WIDTH:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, WHITE, 'consolas', HEIGHT_WIDTH*2)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)