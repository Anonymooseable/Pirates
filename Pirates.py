import pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Yarrrr!!')

board = ((0,1,2,3,4,5),(0,1,2,3,4,5),\
(0,1,2,3,4,5),(0,1,2,3,4,5),(0,1,2,3,4,5),(0,1,2,3,4,5)) #matrix time!
y=3
x=2
K_LEFT=0;K_RIGHT=0;K_DOWN=0;K_UP=0
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
cmd = {K_LEFT:left, K_RIGHT:right, \
K_DOWN:down, K_UP:up} #all possible commands go in here
running=True
while running:
    for user in pygame.event.get():
        if str(user.type)=='KEYDOWN' and user.key in cmd:
            cmd[event.key]()
            print(x,y)
        cursor_pos=board[y][x]  #remember: rows then columns
        if str(user.type)=='QUIT':
            running=False
pygame.quit()
