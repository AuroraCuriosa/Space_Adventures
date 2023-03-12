#
# Space Adventures game
# Copyright (c) 2022 Emily Probin
#
# Contains the main game functions and the main game loop


#This link has information on random numbers for games#
#https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/random-object-generation/ 


import pygame, sys
from math import ceil, sqrt
from random import randint
import game_classes 
from pygame.locals import QUIT
from screen_management import surface, screen_x, screen_y


# Set the title of the window
DISPLAYSURF = pygame.display.set_caption('SPACE ADVENTURE')

# Loads the background image
bg = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
bg_width, bg_height = bg.get_size()

pygame.mouse.set_visible(False)

image_todisplay = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_med3.png")


# https://www.pygame.org/docs/ref/time.html#pygame.time.Clock
FPS = 60
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
pygame.time.set_timer(pygame.USEREVENT, 1 * 60//2 * 1000)


def npc_management(asteroids, chance_asteroidspawn, lasers):
  ''' Decides if an asteroid should be spawned, decides which asteroids and lasers are not alive and deletes them '''
  asteroid_spawn = randint(0, chance_asteroidspawn)
  
  if asteroid_spawn == 0:
    asteroids.append(game_classes.asteroid())
  
  
  # Check for asteroids that are not alive
  if len(asteroids) > 0:
    asteroidsToDelete = []
    for rock in range(len(asteroids)):
      if asteroids[rock].get_alive() == False:
        asteroidsToDelete.append(rock)
    for x in range(len(asteroidsToDelete)):
      del asteroids[asteroidsToDelete[x]]

  # Delete lasers that are not alive
  if len(lasers) > 0:
    #lasersToDelete = []
    need_to_rescan_entire_list = True
    start = 0
    while need_to_rescan_entire_list:
      need_to_rescan_entire_list = False # the for loop might not find any to delete, so assume that is the case until we find one
      
      for x in range(start, len(lasers)):
        if lasers[x].get_alive() == False:
            need_to_rescan_entire_list = True
            del lasers[x]
            start = x
            break # only do one per pass of the list
    
   







def draw(game_score, player, asteroids, surface, image_todisplay):
  ''' Prepares the background and score to be displayed, and moves the asteroids, lasers and player ship '''
  for i in range(ceil(screen_x / bg_width)):
    for j in range(ceil(screen_y / bg_height)):
      surface.blit(bg, ((i * bg_width), (j * bg_height)))
  
  font_colour=(200, 200, 200) 
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",20)
  # Render the objects
  text_obj=font_obj.render("Score: " + str(game_score.get_score()),True,font_colour)
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
  ''' Player Reward and Increased Game difficulty '''
  game_score.addfifty_toscore()
  chance_asteroidspawn = round(chance_asteroidspawn * 0.85, 2)
  #Resets timer so this function is run again in 30 secs
  pygame.time.set_timer(pygame.USEREVENT,  1 * 60//2 * 1000)




def game_main():
  ''' This is the main module, contains the main game loop '''
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
    
    npc_management(asteroids, chance_asteroidspawn, player.lasers)

    
    draw(game_score, player, asteroids, surface, image_todisplay)
    
    
    pygame.display.flip()
