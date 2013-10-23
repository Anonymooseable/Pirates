#!/usr/bin/env python3

import pygame
import pygame as pg
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Yarrrr!!')

board = ((0,1,2,3,4,5),(0,1,2,3,4,5),\
(0,1,2,3,4,5),(0,1,2,3,4,5),(0,1,2,3,4,5),(0,1,2,3,4,5)) #matrix time!
y=3
x=2
def left():
    if x!=0:
        x=x-1
def right():
    if x!=5:
        x=x+1
def down():
    if y!=5:
        y=y+1
def up():
    if y!=0:
        y=y-1    
cmd = {pg.K_LEFT:left, pg.K_RIGHT:right, \
pg.K_DOWN:down, pg.K_UP:up} #all possible commands go in here
running=True
while running:
    for user in pygame.event.get():
        if user.type==pg.KEYDOWN and user.key in cmd:
            cmd[user.key]()
            print(x,y)
        cursor_pos=board[y][x]  #remember: rows then columns
        if user.type==pygame.QUIT:
            running=False
pygame.quit()

