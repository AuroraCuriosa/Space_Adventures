#
# Screen Management
# Copyright © 2023 Emily Probin
# Initialise surface, and some variables for the height and width of the screen
#

import pygame

# Initializing surface - 0, 0 means autodetect ----- Currently Fixed
screen_x = 640
screen_y = 480
surface = pygame.display.set_mode((screen_x, screen_y))


screen_width, screen_height = surface.get_size()