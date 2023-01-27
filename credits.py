#
# Space Adventures game
# Copyright (c) 2022 Emily Probin
#

import pygame, sys
from math import ceil
from pygame.locals import QUIT

pygame.init()  # https://www.pygame.org/docs/ref/pygame.html#pygame.init

# Initializing surface - 0, 0 means autodetect ----- Currently Fixed
screen_x = 640
screen_y = 480
screen = pygame.display.set_mode((screen_x, screen_y))

screen_width, screen_height = screen.get_size()
DISPLAYSURF = pygame.display.set_caption('SPACE ADVENTURE - CREDITS')

FPS = 60
clock = pygame.time.Clock()


def draw():
    pass


def update():
    pass


pygame.display.set_caption('End credits')
screen = pygame.display.set_mode((640, 480))
screen_r = screen.get_rect()
font = pygame.font.Font("Orbitron/orbitron-black.otf", 30)


def temp_main():
    bg = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
    bg_width, bg_height = bg.get_size()

    pygame.display.set_caption('SPACE ADVENTURE - CREDITS')
    pygame.mouse.set_visible(False)
    quit_flag = False

    credit_list = [
        "CREDITS - Space Adventures", " ", "Software Developer - Emily Probin",
        "Senior Programmer - Emily Probin", "Project Manager - Emily Probin",
        "Graphics - Kenney.nl", " ", "Testers", "Emily Probin", "Sarah Burns",
        " ", "Thanks To", "Mr Currie", "Ms Laing", "Rob Probin", "Sarah Burns",
        "Brogan Parry"
    ]

    texts = []
    # we render the text once, since it's easier to work with surfaces
    # also, font rendering is a performance killer
    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (255, 255, 255))
        # we also create a Rect for each Surface.
        # whenever you use rects with surfaces, it may be a good idea to use sprites instead
        # we give each rect the correct starting position
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texts.append((r, s))

    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYUP:
                if e.key == 27:
                    quit_flag = True
                    return quit_flag
        for i in range(ceil(screen_width / bg_width)):
            for j in range(ceil(screen_height / bg_height)):
                screen.blit(bg, ((i * bg_width), (j * bg_height)))

        for r, s in texts:
            # now we just move each rect by one pixel each frame
            r.move_ip(0, -1)
            # and drawing is as simple as this
            screen.blit(s, r)

        # if all rects have left the screen, we exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            return

        # only call this once so the screen does not flicker
        pygame.display.flip()

        # cap framerate at 60 FPS
        clock.tick(60)


#def credits_main():
#  pygame.mouse.set_visible(False)
#  quit_flag = False
#
#
#    draw()
#    update()
