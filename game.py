#
# Space Adventures game
# Copyright (c) 2022 Emily Probin
#

#!!!!!!!!!!!!!!!!!!#
#https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/random-object-generation/ 


import pygame, sys
from math import ceil, sqrt
from random import randint
import game_classes 
from pygame.locals import QUIT

#pygame.init()  # https://www.pygame.org/docs/ref/pygame.html#pygame.init

# Initializing surface - 0, 0 means autodetect ----- Currently Fixed
screen_x = 640
screen_y = 480

surface = pygame.display.set_mode((screen_x, screen_y))

DISPLAYSURF = pygame.display.set_caption('SPACE ADVENTURE')
# Initialing RGB Color
#color = 255, 0, 0
bg = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
bg_width, bg_height = bg.get_size()

pygame.mouse.set_visible(False)




#for i in range(int(bg_width / screen_x)):
#  for j in range(int(bg_height / screen_y)):
#    surface.blit(bg, (i * bg_width), (j * bg_height))
#bg = pygame.transform.scale(bg, (screen_x, screen_y))


# Changing surface color
#surface.fill(color)
#pygame.display.flip()

image_todisplay = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_med3.png")


# https://www.pygame.org/docs/ref/time.html#pygame.time.Clock
FPS = 60
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
pygame.time.set_timer(pygame.USEREVENT, 1 * 60//2 * 1000)


def npc_management(game_score, asteroids, chance_asteroidspawn, lasers):
  asteroid_spawn = randint(0, chance_asteroidspawn)
  
  if asteroid_spawn == 0:
    asteroids.append(game_classes.asteroid())
  
  if len(asteroids) > 0:
    asteroidsToDelete = []
    for rock in range(len(asteroids)):
      if asteroids[rock].get_alive() == False:
        asteroidsToDelete.append(rock)
    for x in range(len(asteroidsToDelete)):
      del asteroids[asteroidsToDelete[x]]

  if len(lasers) > 0:
    lasersToDelete = []
    for x in range(len(lasers)):
      if lasers[x].get_alive() == False:
        lasersToDelete.append(x)
    for x in range(len(lasersToDelete)):
      del lasers[lasersToDelete[x]]







def draw(game_score, player, asteroids, surface, image_todisplay):
  
  for i in range(ceil(screen_x / bg_width)):
    for j in range(ceil(screen_y / bg_height)):
      surface.blit(bg, ((i * bg_width), (j * bg_height)))
  
  font_color=(200, 200, 200) 
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",20)
  # Render the objects
  text_obj=font_obj.render("Score: " + str(game_score.get_score()),True,font_color)
  text_width, text_height = font_obj.size("Score: " + str(game_score.get_score()))
  surface.blit(text_obj,(screen_x - text_width - 10, text_height - 15))

  

  time_sincelastframe =  pygame.time.get_ticks() - start_time

  for x in range(len(asteroids)):
    asteroids[x].move(time_sincelastframe)

  
  for x in range(len(player.lasers)):
    player.lasers[x].move(asteroids, game_score)

  player.move(time_sincelastframe, asteroids)
    # https://www.pygame.org/docs/ref/display.html#pygame.display.update
  #pygame.display.update()
  
  # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
  pygame.display.flip()



def speedup_asteroidspawn(game_score, chance_asteroidspawn):
  game_score.addfifty_toscore()
  chance_asteroidspawn = round(chance_asteroidspawn * 0.85, 2)
  pygame.time.set_timer(pygame.USEREVENT,  1 * 60//2 * 1000)




def game_main():
  pygame.mouse.set_visible(False)
  game_score = game_classes.score() 
  asteroids = []
  chance_asteroidspawn = 60
  player = game_classes.player_ship()
  
  while True:
    clock.tick(FPS)  # limit to at most 60 frames per second

    
    
    for event in pygame.event.get():
      if event.type == pygame.USEREVENT:
        speedup_asteroidspawn(game_score, chance_asteroidspawn)
      
      if event.type == pygame.KEYDOWN:
        #if event.key == 27:
        if event.key == pygame.K_UP:
          player.up_pressed = True
        if event.key == pygame.K_DOWN:
          player.down_pressed = True
        if event.key == pygame.K_LEFT:
          player.left_pressed = True
        if event.key == pygame.K_RIGHT:
          player.right_pressed = True
          
        if event.key == pygame.K_w:
          player.w_pressed = True
          player.shoot_laser()
        if event.key == pygame.K_a:
          player.a_pressed = True
          player.shoot_laser()
        if event.key == pygame.K_s:
          player.s_pressed = True
          player.shoot_laser()
        if event.key == pygame.K_d:
          player.d_pressed = True
          player.shoot_laser()

      if event.type == pygame.KEYUP:
        #if event.key == 27:
        if event.key == pygame.K_UP:
          player.up_pressed = False
        if event.key == pygame.K_DOWN:
          player.down_pressed = False
        if event.key == pygame.K_LEFT:
          player.left_pressed = False
        if event.key == pygame.K_RIGHT:
          player.right_pressed = False
        
        
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYUP:
        if event.key == 27:
          return 0      # no score for abort game

    if player.get_alive() == False:
      return game_score.get_score()
    
    npc_management(game_score, asteroids, chance_asteroidspawn, player.lasers)

    
    draw(game_score, player, asteroids, surface, image_todisplay)
    
    
    pygame.display.flip()
  #  https://www.pygame.org/docs/ref/display.html#pygame.display.update
  #pygame.display.update()
  
  # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
