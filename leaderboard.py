# Leaderboard 
# Copyright © 2023 Emily Probin
# 
#
# https://docs.python.org/3/library/sqlite3.html
# https://www.sqlitetutorial.net/sqlite-python/

import pygame, sys
from pygame.locals import QUIT
from math import ceil
import sqlite3
from sqlite3 import Error
from datetime import date

# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()


# def create_table(conn, create_table_sql):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)




def insertion_sort(values, score_index):
    ''' This sort algorithm sort the leaderboard (high score table) so we can show the top items.
        This is an insertion sort.
    '''
    for index in range (1,len(values)):
        #store the value to be inserted into the array
        current_element = values[index]
        position = index
        #shift the rest of the array one to the right
        while position > 0 and values[position-1][score_index] < current_element[score_index]:
            values[position] = values[position-1]
            position -=1
        #insert the value into the array
        values[position] = current_element

    
    
class Leaderboard:
    ''' This is also called a high score table. This class contains the leaderboard data
        and methods.
    '''
    def __init__(self):
        self._open_db()
    
    
    # https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
    def select_all_leaderboard_data(self):
        """
        Query all rows in the leaderboard table
        :param conn: the Connection object
        :return:
        """
        leaderboard_data = []
        
        cur = self.conn.cursor()
        #cur.execute("SELECT * FROM leaderboard")
        cur.execute("SELECT name, score, date FROM leaderboard")
    
        rows = cur.fetchall()
    
        for row in rows:
            #name, score, date = row
            leaderboard_data.append(row)
        
        return leaderboard_data
    
    
    def do_defaults_exist(self):
        ''' We are checking for a specific default high score set up when the database
        was created'''
        cur = self.conn.cursor()
        cur.execute("""SELECT score FROM leaderboard WHERE name = 'Rob' """)
        rows = cur.fetchall()
        for row in rows:
            if row[0] == 100000:
                return True
            
        return False
            
    def add_default_high_scores(self):
        ''' When the database is created, we add some default values '''
        if not self.do_defaults_exist():
            # default highscores
            self.add_highscore('Rob', 100000)
            self.add_highscore('Emily', 50000)
            self.add_highscore('Peter', 10000)
            self.add_highscore('Johnny', 5000)
            self.add_highscore('Caleb', 1000)
            self.add_highscore('Claire', 500)
            self.add_highscore('Sarah', 100)
            self.add_highscore('Wren', 50)

    
    def _open_db(self):
        ''' Creates a connection with the database and add a leaderboard table, if it doesn't exist '''
        database_filename = "space_adventure_game_data.db"
                
        # create a database connection
        #self.conn = create_connection(database)
        self.conn = sqlite3.connect(database_filename)

        # create tables
        # https://www.sqlite.org/lang_createtable.html#rowid
        
        if self.conn is not None:
            sql_create_leaderboard_table = """ CREATE TABLE IF NOT EXISTS leaderboard (
              id integer PRIMARY KEY,
              name text NOT NULL,
              score integer NOT NULL,
              date TEXT
            ); """
                        # create leaderboard table
            #create_table(self.conn, sql_create_leaderboard_table)
            c = self.conn.cursor()
            c.execute(sql_create_leaderboard_table)
        
            self.add_default_high_scores()

        else:
            print("Error! cannot create the database connection.")
        
        #leaderboard_data = self.select_all_leaderboard_data()
        #print(leaderboard_data)
        #insertion_sort(leaderboard_data)
        
        

    def add_highscore(self, name, score):
        ''' Adds a highscore to the leaderboard table '''
        if self.conn == None:
            self._open_db()

        cur = self.conn.cursor()

        # https://www.sqlite.org/autoinc.html
        
        sql_command = """
                INSERT INTO leaderboard(name, score, date) VALUES
                ( '{}', {}, '{}' ) """.format(name, score, date.today().strftime('%d/%m/%Y'))
        #print(sql_command)
        cur.execute(sql_command)
 
        self.conn.commit()
        
    def get_number_of_highscores(self):
        """ returns the number of highscores """
        return len(self.select_all_leaderboard_data())
        
    def get_top_highscores(self, number_to_return):
        """ returns a (name, score, date) tuple is there is a high score at that index
        or returns None """
        leaderboard_data = self.select_all_leaderboard_data()
        score_index_inside_tuple = 1
        # sort the entries into ascending score. 
        insertion_sort(leaderboard_data, score_index_inside_tuple)
        
        # don't return more entries than actually exist in database
        if number_to_return > len(leaderboard_data):
            number_to_return = len(leaderboard_data)
        
        return leaderboard_data[:number_to_return]
    
    
    

def leaderboard_main(highscores, screen_x, screen_y, bg_width, bg_height, surface, bg):
    ''' The main function for the leaderboard, contains the main loop for the leaderboard '''
    top_5 = highscores.get_top_highscores(5)
    
    display_leaderboard_scores(top_5, screen_x, screen_y, bg_width, bg_height, surface, bg)
    
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYUP:
          if event.key == 27: #Esc
            return 
      


def display_leaderboard_scores(top_5, screen_x, screen_y, bg_width, bg_height, surface, bg):
  ''' Displays the top scores for the leaderboard '''
  for i in range(ceil(screen_x / bg_width)):
    for j in range(ceil(screen_y / bg_height)):
      surface.blit(bg, ((i * bg_width), (j * bg_height)))
     
      
  font_color=(255, 255, 255) 
  font_obj = pygame.font.Font("Orbitron/orbitron-black.otf",30)
  # Render the objects
  text_obj=font_obj.render("Leaderboard",True,font_color)
  text_width, text_height = font_obj.size("Leaderboard")
  surface.blit(text_obj,((screen_x//2) - (text_width//2),(5)))
  
  
  for index in range(0, len(top_5)):
    text_string = str(index + 1) + "    "
    
    for x in range(0, len(top_5[index])):
      #text_obj=font_obj.render(str(top_5[index][x]),True,font_color)
      
      text_string = text_string + " " + str(top_5[index][x])
      
    text_obj=font_obj.render(text_string,True,font_color)
    text_width, text_height = font_obj.size(text_string)
    surface.blit(text_obj,((screen_x//2) - (text_width//2), 100+index*2*text_height))
  
  
  
  
  pygame.display.flip()