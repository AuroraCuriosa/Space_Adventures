# Game Classs
# Copyright © 2023 Emily Probin
# This file holds the classes required by the game. They are score, asteroid, player_ship and laser

import pygame
from math import atan, sin, cos, sqrt
from random import randint
from screen_management import surface, screen_x, screen_y, screen_width, screen_height



#The class that holds the game score
class score():
  ''' This class manages the player score '''
  def __init__(self):
    ''' Start the score '''
    self.score = 0
  def get_score(self):
    ''' For fetching the score '''
    return self.score
  def addten_toscore(self):
    ''' Small score increment. As per classic arcade machines, we 
    always give the player scores multiples of 10. '''
    self.score += 10
  def addfifty_toscore(self):
    ''' Larger score increment. Again a multiple of 10 '''
    self.score += 50





class asteroid():
  ''' The class that forms asteroid objects '''
  def __init__(self):
    ''' Set up asteroid '''
    self.alive = True
    self.aim_point = [0,0]
    self.move_speed_xy = [0,0]
    self.image = pygame.image.load("SpaceShooterRedux/PNG/Meteors/meteorBrown_med3.png")
    self.image_height = self.image.get_height()
    self.image_width = self.image.get_width()
    self.centre_calc = self.image_width // 2, self.image_height // 2
    if self.image_height < self.image_width:
      self.radius = self.image_height // 2
    else:
      self.radius = self.image_width // 2
    
    move_speed = 2

    #defining x,y coords (and off which wall)
    offWhichWall = randint(1,4)

    if offWhichWall <= 2:
      if offWhichWall == 1:
        self.x_coord = 0 - self.image_width
        self.y_coord = randint(0, screen_height - self.image_height)
      else:
        self.x_coord = screen_width
        self.y_coord = randint(0, screen_height - self.image_height)
    else:
      if offWhichWall == 3:
        self.x_coord = randint(0, screen_width - self.image_width)
        self.y_coord = 0 - self.image_height
      else:
        self.x_coord = randint(0, screen_width - self.image_width)
        self.y_coord = screen_height
    

        
    #defining aim wall and point
    self.aim_wall = randint(1,4)
    while self.aim_wall == offWhichWall:
      self.aim_wall = randint(1,4)
    
    if self.aim_wall <= 2:
      if self.aim_wall == 1:
        self.aim_point = [0 - self.image_width, randint(0, screen_height - self.image_height)]
      else:
        self.aim_point = [screen_width, randint(0, screen_height - self.image_height)]
    
    else:
      if self.aim_wall == 3:
        self.aim_point = [randint(0, screen_width - self.image_width), 0 - self.image_height]
      else:
        self.aim_point= [randint(0, screen_width - self.image_width), screen_height]

    
    try:
      angle_formovespeed = atan((self.aim_point[1] - self.y_coord) / (self.aim_point[0] - self.x_coord))
      self.move_speed_xy[1] = move_speed * sin(angle_formovespeed)
      self.move_speed_xy[0] = move_speed * cos(angle_formovespeed)
    except:
      self.move_speed_xy[0] = 0
      self.move_speed_xy[1] = move_speed

  def get_alive(self):
    ''' return whether this asteroid is alive '''
    return self.alive

  def get_coords(self):
    ''' returns coords of top left of image '''
    return self.x_coord, self.y_coord

  def get_end_coords(self):
    ''' get coords of the bottom right of the image '''
    return self.x_coord + self.image_width, self.y_coord + self.image_height

  def explode(self):
    ''' called when the asteroid is no longer alive '''
    self.alive = False
    
  def move(self, frame_time):
    ''' move asteroid in direction decided in init '''
    if not self.alive: return
    self.x_coord += self.move_speed_xy[0] # * round(frame_time/1000,2)
    self.y_coord += self.move_speed_xy[1] # * round(frame_time/1000,2)
    
    if self.aim_wall <= 2:
      if self.aim_wall == 1:
        if self.x_coord < 0 - self.image_width:
          self.alive = False
      else:
        if self.y_coord > screen_width:
          self.alive = False
    else:
      if self.aim_wall == 3:
        if self.y_coord < 0 - screen_height:
          self.alive = False
      else:
        if self.y_coord > screen_height:
          self.alive = False
  
    surface.blit(self.image, (self.x_coord, self.y_coord))









class player_ship():
  ''' The class that forms the player ship '''
  def __init__(self):
    ''' Set up Player Ship '''
    self.alive = True
    self.image = pygame.image.load("SpaceShooterRedux/PNG/playerShip1_blue.png")
    self.image_height = self.image.get_height()
    self.image_width = self.image.get_width()
    self.x_coord = screen_width // 2 - self.image_width // 2
    self.y_coord = screen_height // 2 - self.image_height
    self.up_pressed = False
    self.down_pressed = False
    self.left_pressed = False
    self.right_pressed = False
    self.w_pressed = False
    self.a_pressed = False
    self.s_pressed = False
    self.d_pressed = False
    self.speed = 7
    self.velX = 0
    self.velY = 0 
    self.lasers = [] 
    
    
  def move(self, frame_time, asteroids):
    ''' Move Player Ship '''  
    self.velX = 0
    self.velY = 0
    if self.left_pressed and not self.right_pressed and self.x_coord > 0:
        self.velX = -self.speed
    if self.right_pressed and not self.left_pressed and self.x_coord < screen_width - self.image_width:
        self.velX = self.speed
    if self.up_pressed and not self.down_pressed and self.y_coord > 0:
        self.velY = -self.speed
    if self.down_pressed and not self.up_pressed and self.y_coord < screen_height - self.image_height:
        self.velY = self.speed
    
    self.x_coord += self.velX
    self.y_coord += self.velY
    
    for asteroid in asteroids:
        self.collision_check(asteroid)
    

      
    surface.blit(self.image, (self.x_coord, self.y_coord))
  
  def shoot_laser(self):
    ''' Nothing suprising; we add a laser when this function is called '''
    self.lasers.append(laser(self.x_coord + self.image_width // 2, self.y_coord + self.image_height // 2, self.w_pressed, self.a_pressed, self.s_pressed, self.d_pressed))
    self.w_pressed, self.a_pressed, self.s_pressed, self.d_pressed = False, False, False, False
  
  def get_coords(self):
    ''' get the top left of the player position '''
    return self.x_coord, self.y_coord

  def get_end_coords(self):
    ''' get coords for the bottom right of the player image  '''
    return self.x_coord + self.image_width, self.y_coord + self.image_height

  def get_alive(self):
    ''' return if the player is alive. Other things need to know!!! '''
    return self.alive

  def explode(self):
    ''' Player is dead '''
    self.alive = False
    
      

  def collision_check(self, asteroid):
    ''' Find out whether an asteriod has hit the player '''
    ship_centre = self.x_coord + self.image_width//2, self.y_coord + self.image_height//2
    if self.image_width <= self.image_height:
        ship_radius = self.image_width//2
    else:
        ship_radius = self.image_height//2
     
    asteroid_centre = asteroid.x_coord + asteroid.centre_calc[0], asteroid.y_coord + asteroid.centre_calc[1]
    
    distance = sqrt(((asteroid_centre[0]) - (ship_centre[0]))**2 + ((asteroid_centre[1]) - (ship_centre[1]))**2)
    
    
    if distance <= (ship_radius + asteroid.radius):
      asteroid.explode()
      self.explode()

    
    
    
    
    



class laser():
  ''' Laser class owned by player ship (aggregated relationship) '''
  def __init__(self, x_coord, y_coord, w_pressed, a_pressed, s_pressed, d_pressed):
    ''' initialise the laster data '''
    self.x_coord = x_coord
    self.y_coord = y_coord
    self.direction = [w_pressed, a_pressed, s_pressed, d_pressed]
    self.move_speed = 11
    self.image = pygame.image.load("SpaceShooterRedux/PNG/Lasers/laserBlue03.png")
    if self.direction == [False, True, False, False] or self.direction == [False, False, False, True]:
      self.image = pygame.transform.rotate(self.image, 90) 
    
    self.image_height = self.image.get_height()
    self.image_width = self.image.get_width()
    self.alive = True
    
    
 
  def move(self, asteroids, game_score):
    ''' Move the laser '''
    if self.direction == [True, False, False, False]:
      self.y_coord -= self.move_speed
    elif self.direction == [False, True, False, False]:
      self.x_coord -= self.move_speed
    elif self.direction == [False, False, True, False]:
      self.y_coord += self.move_speed
    elif self.direction == [False, False, False, True]:
      self.x_coord += self.move_speed
      
    
    
    if self.x_coord < 0 or self.x_coord > screen_width or self.y_coord < 0 or self.y_coord > screen_height:
      self.alive = False
    else:
      for asteroid in asteroids:
        self.collision_check(asteroid, game_score)
    
    surface.blit(self.image, (self.x_coord, self.y_coord))

  def get_alive(self):
    ''' return whether this laser is alive '''
    return self.alive

  def get_coords(self):
    ''' return top left coords of laser image '''
    return self.x_coord, self.y_coord

  def get_end_coords(self):
    ''' return bottom left coords of laser image '''
    return self.x_coord + self.image_width, self.y_coord + self.image_height
    
  def explode(self):
    ''' explode in this case means laser is destroyed'''
    self.alive = False    

  def collision_check(self, asteroid, game_score):
    ''' has the laser collided with an asteroid? If it has, increase the game score. '''
    if self.image_height > self.image_width:
      laser_end1 = self.x_coord + self.image_width // 2, self.y_coord
      laser_end2 = self.x_coord + self.image_width // 2, self.y_coord + self.image_height
    else:
      laser_end1 = self.x_coord, self.y_coord + self.image_height // 2
      laser_end2 = self.x_coord + self.image_width, self.y_coord + self.image_height // 2
         
    asteroid_centre = asteroid.x_coord + asteroid.centre_calc[0], asteroid.y_coord + asteroid.centre_calc[1]
    
    distance1 = sqrt(((asteroid_centre[0]) - (laser_end1[0]))**2 + ((asteroid_centre[1]) - (laser_end1[1]))**2)
    distance2 = sqrt(((asteroid_centre[0]) - (laser_end2[0]))**2 + ((asteroid_centre[1]) - (laser_end2[1]))**2)
    
    if distance1 < asteroid.radius or distance2 < asteroid.radius:
      game_score.addten_toscore()
      asteroid.explode()
      self.explode()
      