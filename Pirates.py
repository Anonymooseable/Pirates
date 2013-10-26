#!/usr/bin/env python3

import pygame
import pygame as pg
import random
class PiratesGame:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_rect = 0
        self.y_rect = 0
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
        self.key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up,
            pg.K_ESCAPE: escape
        } # all commands
        self.x_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.y_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.board = [[0 for y in range(6)] for x in range(6)]

        self.running = False

    def run(self):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((600, 600))#Creating a display creates a default surface: here we called it screen.(remember: 25px on sides, 20px between squares, 75px per square and half a square=37px 
        pygame.display.set_caption('Yarrrr!!')
        self.screen.fill((90,50,5))

#Generating ship positions
        generated=False
        X=0
        Y=1
        ship_posx=1
        ship_posy=1
        # Notes for ship generation:
        # 0 = Square free
        # 1 = Ship here
        for ship_length in [2, 3, 3, 4]:
            generated = False
            while not generated:
                x_or_y=random.choice((X, Y)) # Whether ship is horizontal (X) or vertical (Y)
                if x_or_y == X: # The ship is horizontal so we'll mess with the X coordinate
                    ship_posx=random.randint(0,5-ship_length) # Subtract the number of the ship, equivalent to its length (?)
                    ship_posy=random.randint(0,5)
                    generated = True # We'll be doing well until we fail (if we do)
                    for position_on_ship in range(0, ship_length+1): # position_on_ship = how far along the ship we are
                        x = ship_posx + position_on_ship # Determine x coordinate of the next square we want to set as part of the ship
                        if self.board[x][ship_posy]!=0: # If we can't put our ship here
                            generated = False # Then we failed.
                    if generated: # This will only be true if nothing failed - that means we can mark the squares as occupied
                        for position_on_ship in range(ship_length+1): # Same as before
                            x = ship_posx + position_on_ship
                            self.board[x][ship_posy] = 1 # We are now occupying the square!

                else:
                    ship_posx=random.randint(0,5)
                    ship_posy=random.randint(0,5-ship_length) # Subtract the number of the ship, equivalent to its length (?)
                    generated = True # We'll be doing well until we fail (if we do)
                    for position_on_ship in range(0, ship_length+1): # position_on_ship = how far along the ship we are
                        y = ship_posy + position_on_ship # Determine x coordinate of the next square we want to set as part of the ship
                        if self.board[ship_posx][y]!=0: # If we can't put our ship here
                            generated = False # Then we failed.
                    if generated: # This will only be true if nothing failed - that means we can mark the squares as occupied
                        for position_on_ship in range(ship_length+1): # Same as before
                            y = ship_posy + position_on_ship
                            self.board[ship_posx][y] = 1 # We are now occupying the square!

#Drawing the board
        for x, x_pixels in [(0,0),(1,95),(2,190),(3,285),(4,380),(5,475)]:
            for y, y_pixels in [(0,0),(1,95),(2,190),(3,285),(4,380),(5,475)]:
                rect=pygame.Rect(25+x_pixels,25+y_pixels,75,75)  #(x,y,width,height)
                if self.board[x][y] == 0: # If the square is free, draw it blue
                    self.screen.fill((20,70,130),rect)
                else: # Otherwise grey
                    self.screen.fill((128,128,128),rect)
        copy_screen=pygame.Surface.copy(self.screen)
        pygame.display.flip()

        #check whether this works!!
        for y in [0,1,2,3,4,5]:
            for x in [0,1,2,3,4,5]:
                if self.board[y][x]==1:
                    print(x,y)


        curs = pygame.sprite.Sprite()
        curs.image = pygame.image.load("Cross hair.png").convert_alpha()
        curs.rect = curs.image.get_rect()

        while self.running:
            for user in pygame.event.get():
                if user.type==pg.KEYDOWN and user.key in self.key_handlers:
                    self.key_handlers[user.key](self)

                self.screen.blit(copy_screen,(0,0))
                self.screen.blit(curs.image,(self.x_box[self.x],self.y_box[self.y]))
                pygame.display.flip()

                if user.type == pygame.QUIT:
                    self.running = False
        pygame.quit()


if __name__ == "__main__":
    PiratesGame().run()
