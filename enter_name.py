import pygame
import sys
from math import ceil
from time import sleep

screen_width = 640
screen_height = 480
surface = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.image.load("SpaceShooterRedux/Backgrounds/darkPurple.png")
bg_width, bg_height = bg.get_size()

# text entry
# https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

def main(highscores, score):
  clock = pygame.time.Clock()
  pygame.mouse.set_visible(True)
  text_list = []
  FPS = 60
  typing = True
  button_text_coords = [0,0,0,0]
  pos_mouse_click = [640,480]
  
  display_background()
  sleep(2)
    
  while typing:
    button_text_coords = draw(text_list, button_text_coords)
    
    if len(text_list) > 0:
      typing = detect_button_press(button_text_coords, pos_mouse_click)
    
    clock.tick(FPS)  # limit to at most 60 frames per second

  
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        pos_mouse_click = list(pygame.mouse.get_pos())
        #print(pos_mouse_click)

      if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_RETURN:
          if len(text_list) > 0:
            typing = False

        elif event.key == pygame.K_BACKSPACE:
          if len(text_list) > 0:
              text_list = text_list[:-1]
      
        else:
            if len(text_list) < 10 and event.unicode != "" and ord(event.unicode) >= 32:
                #print(event.unicode)
                text_list.append(event.unicode)

    
    pygame.display.flip()

  # add highscore
  selected_name = ''.join(text_list)
  if len(selected_name) > 0:
    highscores.add_highscore(selected_name, score)
    
    
    
def draw(text_list, button_text_coords):
    display_background()
    display_text(text_list)
    button_text_coords = display_enter_button(button_text_coords)
    
    return button_text_coords
    
def display_background():
  for i in range(ceil(screen_width / bg_width)):
    for j in range(ceil(screen_height / bg_height)):
      surface.blit(bg, ((i * bg_width), (j * bg_height)))



def display_text(text_list):
  text = ''.join(text_list)
  
  font_color=(255, 255, 255) 
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",45)
  # Render the objects
  
  if len(text) > 0:
      text_obj=font_obj.render(str(text),True,font_color)
      text_width, text_height = font_obj.size(str(text))
      surface.blit(text_obj,((screen_width//2) - (text_width//2),(screen_height//4) - (text_height//2)))
  
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",25)  
    
  text_obj=font_obj.render("Type your name here for the leaderboard:",True,font_color)
  text_width, text_height = font_obj.size(str(text))
  surface.blit(text_obj,(5,5))
    

def display_enter_button(button_text_coords):
  font_color=(190, 190, 190) 
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",30)
  # Render the objects
  text_obj=font_obj.render("Enter",True,font_color)
  text_width, text_height = font_obj.size("Enter")
  button_text_coords = [(screen_width//2) - (text_width//2),(screen_height//4*3) - (text_height//2), (screen_width//2) - (text_width//2) + text_width, (screen_height//4*3) - (text_height//2) + text_height]
  
  
  surface.blit(text_obj,((screen_width//2) - (text_width//2),(screen_height//4*3) - (text_height//2)))
  
  return button_text_coords
  

def detect_button_press(button_text_coords, pos_mouse_click):
    if pos_mouse_click[0] >= button_text_coords[0] and pos_mouse_click[0] <= button_text_coords[2] and pos_mouse_click[1] >= button_text_coords[1] and pos_mouse_click[1] <= button_text_coords[3]:
        return False
    else:
        return True