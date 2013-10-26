#!/usr/bin/env python3

import pygame
import pygame as pg

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
        self.running = False

    def run(self):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((600, 600))#Creating a display creates a default surface: here we called it screen.(remember: 25px on sides, 20px between squares, 75px per square and half a square=37px 
        pygame.display.set_caption('Yarrrr!!')
        self.screen.fill((90,50,5))

        for self.x_rect in [0,95,190,285,380,475]:
            for self.y_rect in [0,95,190,285,380,475]:
                rect=pygame.Rect(25+self.x_rect,25+self.y_rect,75,75)  #(x,y,width,height)
                self.screen.fill((20,70,130),rect)
        curs_surf=pygame.Surface(self.screen.get_size(),pygame.SRCALPHA) #Creating cursor surface: the cursor shall draw on here.
        curs_surf.fill((0,0,0,255))
        pygame.display.flip()
        
        curs = pygame.sprite.Sprite()
        curs.image = pygame.image.load("Cross hair.png").convert_alpha()
        curs.rect = curs.image.get_rect()

        while self.running:
            for user in pygame.event.get():
                if user.type==pg.KEYDOWN and user.key in self.key_handlers:
                    self.key_handlers[user.key](self)
                    print (self.x, self.y)
                    curs_surf.fill((0,0,0,255))
                    curs_surf.blit(curs.image,(self.x_box[self.x],self.y_box[self.y]),curs.rect,pygame.BLEND_RGBA_ADD)
                    pygame.display.flip()
                    
                if user.type == pygame.QUIT:
                    self.running = False
        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
