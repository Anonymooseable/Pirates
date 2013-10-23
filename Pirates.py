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
        self.x_box = {0:62,1:157,2:252,3:347,4:442,5:537}
        self.y_box = {0:62,1:157,2:252,3:347,4:442,5:537}
        self.running = False

    def run(self):
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((600, 600))#25px on sides, 20px 
        pygame.display.set_caption('Yarrrr!!')           #between squares and
                                                         #75px per square and half a square=37px
        for self.x_rect in [0,95,190,285,380,475]:
            for self.y_rect in [0,95,190,285,380,475]:
                rect=pygame.Rect(25+self.x_rect,25+self.y_rect,75,75)  #(x,y,width,height)
                self.screen.fill((250,250,250),rect)
        pygame.display.flip()

        while self.running:
            for user in pygame.event.get():
                if user.type==pg.KEYDOWN and user.key in self.key_handlers:
                    self.key_handlers[user.key](self)
                    print (self.x, self.y)
                    cursor_pos = [self.x_box[self.x],self.y_box[self.y]]
                    print (cursor_pos)
                if user.type == pygame.QUIT:
                    self.running = False
        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()
