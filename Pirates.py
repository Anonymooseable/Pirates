#!/usr/bin/env python3

import pygame
import pygame as pg
import random
class PiratesGame:
    def __init__(self):
        pygame.init()
        #Images--------------------------
        self.screen = pygame.display.set_mode((600, 600))#Creating a display creates a default surface: here we called it screen.(remember: 25px on sides, 20px between squares, 75px per square and half a square=37px 
        pygame.display.set_caption('Yarrrr!!')

        self.curs = pygame.sprite.Sprite()
        self.curs.image = pygame.image.load("Cross hair.png").convert_alpha()
        self.curs.rect = self.curs.image.get_rect()

        self.box = pygame.sprite.Sprite()
        self.box.image = pygame.image.load("box.png").convert_alpha()
        self.box.rect = self.box.image.get_rect()

        self.boardfile = pygame.sprite.Sprite()
        self.boardfile.image = pygame.image.load("board.png").convert_alpha()
        self.boardfile.rect = self.boardfile.image.get_rect()

        self.parch = pygame.sprite.Sprite()
        self.parch.image = pygame.image.load("parchment_75%.png").convert_alpha()
        self.parch.rect = self.parch.image.get_rect()
        
        self.screen.blit(self.boardfile.image,(0,0))
        
        self.copy_screen=pygame.Surface.copy(self.screen)
        #Vars----------------------------
        self.x = 0
        self.y = 0
        self.x_rect = 0
        self.y_rect = 0
        #Functions-----------------------
        def left(self):
            if self.x != 0:
                self.x -= 1
        def right(self):
            if self.x != 5:
                self.x += 1
        def down(self):
            if self.y != 5:
                self.y += 1
        def up(self):
            if self.y!=0:
                self.y -= 1
        def escape(self):
            self.running = False
        def fire(self):
            if self.board[self.x][self.y]==0:
                self.screen.blit(self.copy_screen,(0,0))
                rect=pygame.Rect(self.x_box[self.x],self.y_box[self.y],75,75)
                self.screen.fill((90,170,190),rect)
                self.copy_screen=pygame.Surface.copy(self.screen)
            else:
                self.screen.blit(self.copy_screen,(0,0))
                rect=pygame.Rect(self.x_box[self.x],self.y_box[self.y],75,75)
                self.screen.fill((240,150,75),rect)
                self.copy_screen=pygame.Surface.copy(self.screen)
        #Other---------------------------
        self.key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up,
            pg.K_ESCAPE: escape,
            pg.K_RETURN: fire
        } # all commands
        self.x_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.y_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.board = [[0 for y in range(6)] for x in range(6)]

        self.running = False

    def run(self):

        self.running = True
        

#Generating ship positions
        generated=False
        ship_posx=1
        ship_posy=1
        # Notes for ship generation:
        # 0 = Square free
        # 1 = Ship here
        ships = ((1, 2), (2, 3), (3, 3), (4, 4)) # Make an ID and a length for 4 ships
        for ship_id, ship_length in ships:
            generated = False
            while not generated:
                x_or_y=random.choice(('horizontal','vertical'))
                if x_or_y == 'horizontal': 
                    ship_posx=random.randint(0,5-ship_length) # Subtract the length of the ship
                    ship_posy=random.randint(0,5)
                    generated = True # We'll be doing well until we fail (if we do)
                    for position_on_ship in range(0, ship_length): # position_on_ship = how far along the ship we are
                        x = ship_posx + position_on_ship # Determine x coordinate of the next square we want to set as part of the ship
                        if self.board[x][ship_posy]!=0: # If we can't put our ship here
                            generated = False # Then we failed.
                    if generated: # This will only be true if nothing failed - that means we can mark the squares as occupied
                        for position_on_ship in range(ship_length): # Same as before
                            x = ship_posx + position_on_ship
                            self.board[x][ship_posy] = ship_id # We are now occupying the square!

                else:
                    ship_posx=random.randint(0,5)
                    ship_posy=random.randint(0,5-ship_length) # Subtract the length of the ship
                    generated = True # We'll be doing well until we fail (if we do)
                    for position_on_ship in range(0, ship_length): # position_on_ship = how far along the ship we are
                        y = ship_posy + position_on_ship # Determine x coordinate of the next square we want to set as part of the ship
                        if self.board[ship_posx][y]!=0: # If we can't put our ship here
                            generated = False # Then we failed.
                    if generated: # This will only be true if nothing failed - that means we can mark the squares as occupied
                        for position_on_ship in range(ship_length): # Same as before
                            y = ship_posy + position_on_ship
                            self.board[ship_posx][y] = ship_id # We are now occupying the square!
   #Drawing the board
        for x, x_pixels in self.x_box.items():
            for y, y_pixels in self.y_box.items():
                rect=pygame.Rect(x_pixels,y_pixels,75,75)#(x,y,width,height)
                if self.board[x][y] == 0: # If the square is free, draw it blue
                    self.screen.blit(self.box.image,(x_pixels,y_pixels))
                else: # Otherwise grey
                    c = pygame.Color(0, 0, 0)
                    value = min(25 + 12*self.board[x][y], 100) # Value between 0 and 100
                    c.hsva = (0, 0, value, 100)
                    self.screen.fill(c,rect)
        self.screen.blit(self.parch.image,(0,0),None,pg.BLEND_RGBA_MULT)
        pygame.display.flip()
        self.copy_screen=pygame.Surface.copy(self.screen)
        

        while self.running:
            for user in pygame.event.get():
                if user.type==pg.KEYDOWN and user.key in self.key_handlers:
                    self.key_handlers[user.key](self)

                self.screen.blit(self.copy_screen,(0,0))
                self.screen.blit(self.curs.image,(self.x_box[self.x],self.y_box[self.y]))
                pygame.display.flip()

                if user.type == pygame.QUIT:
                    self.running = False
        pygame.quit()


if __name__ == "__main__":
    PiratesGame().run()
