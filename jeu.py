"""
Snake Eater
Made with PyGame
"""
import pygame
import sys
import time
import random
from typing import List, Tuple
from game import *


# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Main logic
game = Game()
while not game.is_ended():
    game.update(pygame.time.Clock())

    game.render(game_window)
    