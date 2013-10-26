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
        self.key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up
        } # all commands
        self.x_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.y_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.board = ({0:0,1:0,2:0,3:0,4:5,5:0},{0:0,1:0,2:0,3:0,4:0,5:0},{0:0,1:0,2:0,3:0,4:0,5:0},
                      {0:0,1:0,2:0,3:0,4:0,5:0},{0:0,1:0,2:0,3:0,4:0,5:0},{0:0,1:0,2:0,3:0,4:0,5:0}) #y=row=choose dict then x=column=choose element in dict
        
        self.running = False

    def run(self):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((600, 600))#Creating a display creates a default surface: here we called it screen.(remember: 25px on sides, 20px between squares, 75px per square and half a square=37px 
        pygame.display.set_caption('Yarrrr!!')
        self.screen.fill((90,50,5))

#Drawing the board
        for self.x_rect in [0,95,190,285,380,475]:
            for self.y_rect in [0,95,190,285,380,475]:
                rect=pygame.Rect(25+self.x_rect,25+self.y_rect,75,75)  #(x,y,width,height)
                self.screen.fill((20,70,130),rect)
        copy_screen=pygame.Surface.copy(self.screen)
        pygame.display.flip()
        
        curs = pygame.sprite.Sprite()
        curs.image = pygame.image.load("Cross hair.png").convert_alpha()
        curs.rect = curs.image.get_rect()

#Generating ship positions
        not_generated=True
        ship_posx=1
        ship_posy=1
        for ship_nb in range(1,4):
            while not_generated:
                loop=False
                x_or_y=random.choice((ship_posx,ship_posy))
                if x_or_y == ship_posx:
                    ship_posy=random.randint(0,5)
                    ship_posx=random.randint(0,5-ship_nb)
                    if self.board[ship_posy][ship_posx]==0:
                        self.board[ship_posy][ship_posx]=1
                        not_generated=False
                    else:
                        loop=True

                    for blarg in range(1,ship_nb+1):
                        x_or_y=x_or_y+blarg
                        if self.board[ship_posy][ship_posx]==0:
                            self.board[ship_posy][ship_posx]=1
                            not_generated=False
                        else:
                            loop=True
                else:
                    ship_posy=random.randint(0,5-ship_nb)
                    ship_posx=random.randint(0,5)
                    if self.board[ship_posy][ship_posx]==0:
                        self.board[ship_posy][ship_posx]=1
                        not_generated=False
                    else:
                        loop=True

                    for blarg in range(1,ship_nb+1):
                        x_or_y=x_or_y+blarg
                        if self.board[ship_posy][ship_posx]==0:
                            self.board[ship_posy][ship_posx]=1
                            not_generated=False
                        else:
                            loop=True
                if loop:
                    not_generated=True
            
    
                            
                    
        #check whether this works!!
        for y in [0,1,2,3,4,5]:
            for x in [0,1,2,3,4,5]:
                if self.board[y][x]==1:
                    print(x,y)
                    
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
