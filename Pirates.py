#!/usr/bin/env python3

import pygame
import pygame as pg

class PiratesGame:
    def __init__(self):
        self.x = 0
        self.y = 0
        def left(self):
            if self.x!=0:
                self.x -= 1
        def right(self):
            if self.x!=5:
                self.x += 1
        def down(self):
            if self.y!=5:
                self.y += 1
        def up(self):
            if self.y!=0:
                self.y -= 1
        self.key_handlers = {
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up
        }

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Yarrrr!!')

        board = ((0,1,2,3,4,5),(0,1,2,3,4,5),\
        (0,1,2,3,4,5),(0,1,2,3,4,5),(0,1,2,3,4,5),(0,1,2,3,4,5)) #matrix time!
        y=3
        x=2

        running=True
        while running:
            for user in pygame.event.get():
                if user.type==pg.KEYDOWN and user.key in self.key_handlers:
                    self.key_handlers[user.key](self)
                    print(x,y)
                cursor_pos=board[y][x]  #remember: rows then columns
                if user.type==pygame.QUIT:
                    running=False
        pygame.quit()

if __name__ == "__main__":
    PiratesGame().run()