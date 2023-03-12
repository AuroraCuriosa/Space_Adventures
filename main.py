#
# Space Adventures game
# Copyright (c) 2022 Emily Probin
#

import pygame, sys
from math import ceil
from pygame.locals import QUIT
import game
import credits
import leaderboard
import enter_name
from screen_management import surface, screen_x, screen_y, screen_width, screen_height

pygame.init()  


DISPLAYSURF = pygame.display.set_caption('SPACE ADVENTURE')
bg = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
bg_width, bg_height = bg.get_size()

pygame.mouse.set_visible(True)




#Module to prepare the background to the display
def display_background():
  for i in range(ceil(screen_width / bg_width)):
    for j in range(ceil(screen_height / bg_height)):
      surface.blit(bg, ((i * bg_width), (j * bg_height)))





#Module to prepart the button text to be displayed
def display_text(text_coords):
  
  #White text colour
  font_colour=(255, 255, 255) 
  #Declare font
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",35)
  
  
  # Render the objects (in this case, it's the text)
  text_obj=font_obj.render("Start Game",True,font_colour)
  text_width, text_height = font_obj.size("Start Game")
  surface.blit(text_obj,((screen_x//2) - (text_width//2),(screen_y//4) - (text_height//2)))
  text_coords[0] = [(screen_x//2) - (text_width//2),(screen_y//4) - (text_height//2), text_width, text_height]
  
  text_obj=font_obj.render("Leaderboard",True,font_colour)
  text_width, text_height = font_obj.size("Leaderboard")
  surface.blit(text_obj,((screen_x//2) - (text_width//2),(screen_y//4*2) - (text_height//2)))
  text_coords[1] = [(screen_x//2) - (text_width//2),(screen_y//4*2) - (text_height//2), text_width, text_height]
  
  
  text_obj=font_obj.render("Credits",True,font_colour)
  text_width, text_height = font_obj.size("Credits")
  surface.blit(text_obj,((screen_x//2) - (text_width//2),(screen_y//4*3) - (text_height//2)))
  text_coords[2] = [(screen_x//2) - (text_width//2),(screen_y//4*3) - (text_height//2), text_width, text_height]




#Function to convert the length of the button into the coords of the end of the button
def convert_lengthbutton_tocoords(text_coords):
  for x in range(0,3):
    text_coords[x][2] = text_coords[x][2] + text_coords[x][0]
    text_coords[x][3] = text_coords[x][3] + text_coords[x][1]
  




highscores = leaderboard.Leaderboard()
#test code
#print("Number of highscores =", highscores.get_number_of_highscores())
#print(highscores.get_top_highscores(10))
#print(highscores.get_top_highscores(4))
#highscores.add_highscore("Fred", 60000)
#print(highscores.get_top_highscores(4))
#highscores.add_highscore("Rob", 1)
#highscores.add_highscore("George", 1)
#print(highscores.get_top_highscores(4))
#highscores.add_highscore("Sid", 100000000)
#highscores.add_highscore("Claier", 999996)
#highscores.add_highscore("Claire", 999998)
#print(highscores.get_top_highscores(10))
#


#Check for if the mouse has clicked a button
#This is what changes them from text to functional buttons
def has_mouse_clicked_button(pos_mouse_click, text_coords):
  #if mouse has clicked 'Start Game'
  if pos_mouse_click[0] >= text_coords[0][0] and pos_mouse_click[0] <= text_coords[0][2] and pos_mouse_click[1] >= text_coords[0][1] and pos_mouse_click[1] <= text_coords[0][3]:
    score = game.game_main()
    if score != 0:
        enter_name.main(highscores, score)
    pygame.mouse.set_visible(True)
    
  #if not
  #has mouse clicked 'Leaderboard'  
  elif pos_mouse_click[0] >= text_coords[1][0] and pos_mouse_click[0] <= text_coords[1][2] and pos_mouse_click[1] >= text_coords[1][1] and pos_mouse_click[1] <= text_coords[1][3]:
    leaderboard.leaderboard_main(highscores, screen_x, screen_y, bg_width, bg_height, surface, bg)
    pygame.display.set_caption('SPACE ADVENTURE')
  
  #if neither
  #has mouse clicked 'Credits'
  elif pos_mouse_click[0] >= text_coords[2][0] and pos_mouse_click[0] <= text_coords[2][2] and pos_mouse_click[1] >= text_coords[2][1] and pos_mouse_click[1] <= text_coords[2][3]:
    credits.credits_main()
    pygame.display.set_caption('SPACE ADVENTURE')
    pygame.mouse.set_visible(True)
    






#set frames per second
FPS = 60
clock = pygame.time.Clock()

#initialise variables to be used later (these ones are used to make the buttons functional)
text_coords = [[0] * 3 for i in range(4)]
pos_mouse_click = [0, 0]


## main module ##
while True:
  clock.tick(FPS)  # limit to at most 60 frames per second
  
  #prepare background for display
  display_background()
  
  #prepare text for display
  display_text(text_coords)
  
  #Change length of buttons to the coords of the end of the buttons
  convert_lengthbutton_tocoords(text_coords)
  
  #Detect QUIT event and if the mouse has been pressed (if the mouse has been clicked get coords)
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONUP:
      pos_mouse_click = list(pygame.mouse.get_pos())
  
  #Check if the mouse has clicked a button, act accordingly, and reset the variable that holds the coords
  has_mouse_clicked_button(pos_mouse_click, text_coords)
  pos_mouse_click = [0,0]
  
  #Display the data we have prepared
  pygame.display.flip()
