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

        self.splash = pygame.sprite.Sprite()
        self.splash.image = pygame.image.load("splash.png").convert_alpha()
        self.splash.rect = self.splash.image.get_rect()

        self.screen.blit(self.boardfile.image,(0,0))

        self.copy_screen=pygame.Surface.copy(self.screen)
        self.ani_copy_screen=pygame.Surface.copy(self.screen)
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
            # Todo: make it change to pause menu state instead
        def fire(self):
            if self.board[self.x][self.y]==-1:
                self.screen.blit(self.copy_screen,(0,0))
                for blarg in range(0,35):
                    rect=pygame.Rect(0+blarg*75,0,75,75)
                    self.screen.blit(self.splash.image,(self.x_box[self.x],self.y_box[self.y]),rect)
                    self.screen.blit(self.parch.image,(self.x_box[self.x],self.y_box[self.y]),rect,pg.BLEND_RGBA_MULT)
                    pygame.display.flip()
                self.copy_screen=pygame.Surface.copy(self.screen)
            else:
                self.screen.blit(self.copy_screen,(0,0))
                rect=pygame.Rect(self.x_box[self.x],self.y_box[self.y],75,75)
                self.screen.fill((240,150,75),rect)
                self.screen.blit(self.parch.image,(0,0),None,pg.BLEND_RGBA_MULT)
                self.copy_screen=pygame.Surface.copy(self.screen)
        #Other---------------------------
        self.key_handlers = {   # all commands
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up,
            pg.K_ESCAPE: escape,
            pg.K_RETURN: fire
        }
        self.x_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.y_box = {0:25,1:120,2:215,3:310,4:405,5:500}
        self.board = [[-1 for y in range(6)] for x in range(6)]

        #Generating ship positions
        # Notes for board contents:
        # -1 = Square free
        # >= 0 = Ship here
        for ship_id, ship_length in enumerate([2, 3, 3, 4]):
            generated = False
            while not generated:
                x_or_y=random.choice(('horizontal','vertical'))
                if x_or_y == 'horizontal':
                    ship_posx=random.randint(0,5-ship_length) # Subtract the length of the ship
                    ship_posy=random.randint(0,5)
                    generated = True # We'll be doing well until we fail (if we do)
                    for position_on_ship in range(0, ship_length): # position_on_ship = how far along the ship we are
                        x = ship_posx + position_on_ship # Determine x coordinate of the next square we want to set as part of the ship
                        if self.board[x][ship_posy] != -1: # If we can't put our ship here
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
                        if self.board[ship_posx][y] != -1: # If we can't put our ship here
                            generated = False # Then we failed.
                    if generated: # This will only be true if nothing failed - that means we can mark the squares as occupied
                        for position_on_ship in range(ship_length): # Same as before
                            y = ship_posy + position_on_ship
                            self.board[ship_posx][y] = ship_id # We are now occupying the square!

        # Drawing the board
        for x, x_pixels in self.x_box.items():
            for y, y_pixels in self.y_box.items():
                rect=pygame.Rect(x_pixels,y_pixels,75,75)#(x,y,width,height)
                if self.board[x][y] == -1: # If the square is free, draw it blue
                    self.screen.blit(self.box.image,(x_pixels,y_pixels))
                else: # Otherwise grey
                    c = pygame.Color(0, 0, 0)
                    value = min(25 + 12*self.board[x][y], 100) # Value between 0 and 100
                    c.hsva = (0, 0, value, 100)
                    self.screen.fill(c,rect)
        self.copy_screen=pygame.Surface.copy(self.screen)#Blank copy of board without the multiply on it
        self.screen.blit(self.parch.image,(0,0),None,pg.BLEND_RGBA_MULT)
        pygame.display.flip()
        self.copy_screen=pygame.Surface.copy(self.screen)

        # Set up main menu
        self.menu_item_heights = [50, 150, 250, 350, 450]
        self.menu_font = pygame.font.Font("FortuneCookieNF.ttf", 48)
        def menu_text(text):
            return self.menu_font.render(text, True, (255, 255, 255))
        self.menu_select_marker = menu_text(">")

        self.main_menu_image = pygame.Surface(self.screen.get_size())
        self.main_menu_start = menu_text("Start Game")
        self.main_menu_easy = menu_text("Easy >")
        self.main_menu_medium = menu_text("< Medium >")
        self.main_menu_hard = menu_text("< Hard")
        self.main_menu_quit = menu_text("Quit")
        self.main_menu_sel = 0
        self.main_menu_difficulty = 0 # 0 = easy, 1 = medium, 2 = hard

        self.quit_menu_image = pygame.Surface(self.screen.get_size())
        self.quit_menu_really = menu_text("Really quit?")
        self.quit_menu_yes = menu_text("Yes")
        self.quit_menu_no = menu_text("No")
        self.quit_menu_confirm = True

        self.running = False
        self.state = "main menu"
        self.redraw_main_menu()
        self.draw_quit_menu()

    def redraw_main_menu(self):
        self.main_menu_image.fill((0, 0, 0))
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        self.main_menu_image.blit(self.main_menu_start, (center_horiz_pos(self.main_menu_start), self.menu_item_heights[0]))
        if self.main_menu_difficulty == 0:
            difficulty_image = self.main_menu_easy
        elif self.main_menu_difficulty == 1:
            difficulty_image = self.main_menu_medium
        elif self.main_menu_difficulty == 2:
            difficulty_image = self.main_menu_hard
        self.main_menu_image.blit(difficulty_image, (center_horiz_pos(difficulty_image), self.menu_item_heights[1]))
        self.main_menu_image.blit(self.main_menu_quit, (center_horiz_pos(self.main_menu_quit), self.menu_item_heights[2]))

    def draw_quit_menu(self):
        self.quit_menu_image.fill((0, 0, 0))
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        self.quit_menu_image.blit(self.quit_menu_really, (center_horiz_pos(self.quit_menu_really), self.menu_item_heights[0]))
        self.quit_menu_image.blit(self.quit_menu_yes, (center_horiz_pos(self.quit_menu_yes), self.menu_item_heights[1]))
        self.quit_menu_image.blit(self.quit_menu_no, (center_horiz_pos(self.quit_menu_no), self.menu_item_heights[2]))

    def run(self):
        self.running = True
        clock=pygame.time.Clock()
        while self.running:
            clock.tick(25)
            if self.state == "main menu":
                for event in pygame.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP: # Move menu cursor up
                            self.main_menu_sel -= 1
                            self.main_menu_sel %= 3 # Wrap around if it's out of bounds
                        elif event.key == pg.K_DOWN: # Move menu cursor down
                            self.main_menu_sel += 1
                            self.main_menu_sel %= 3
                        elif event.key == pg.K_ESCAPE:
                            self.main_menu_sel = 2
                        elif event.key == pg.K_RETURN:
                            if self.main_menu_sel == 0: # Start
                                self.state = "targeting"
                            elif self.main_menu_sel == 1: # Difficulty
                                self.main_menu_difficulty += 1
                                self.main_menu_difficulty %= 3
                            elif self.main_menu_sel == 2:
                                self.state = "quit menu"
                                self.old_state = "main menu"
                        elif event.key == pg.K_LEFT and self.main_menu_sel == 1 and self.main_menu_difficulty > 0:
                            self.main_menu_difficulty -= 1
                            self.redraw_main_menu()
                        elif event.key == pg.K_RIGHT and self.main_menu_sel == 1 and self.main_menu_difficulty < 2:
                            self.main_menu_difficulty += 1
                            self.redraw_main_menu()
                self.screen.blit(self.main_menu_image, (0, 0))
                self.screen.blit(self.menu_select_marker, (10, self.menu_item_heights[self.main_menu_sel]))
            elif self.state == "quit menu":
                for event in pygame.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key in (pg.K_DOWN, pg.K_UP): # The menu has two items so pressing up or down works out to the same thing
                            self.quit_menu_confirm = not self.quit_menu_confirm
                        elif event.key == pg.K_RETURN:
                            if self.quit_menu_confirm:
                                self.running = False
                            else:
                                self.state = self.old_state
                self.screen.blit(self.quit_menu_image, (0, 0))
                self.screen.blit(self.menu_select_marker, (10, self.menu_item_heights[int(not self.quit_menu_confirm) + 1]))

            elif self.state == "targeting":
                for event in pygame.event.get():
                    if event.type==pg.KEYDOWN and event.key in self.key_handlers:
                        self.key_handlers[event.key](self)

                    self.screen.blit(self.copy_screen,(0,0))
                    self.screen.blit(self.curs.image,(self.x_box[self.x],self.y_box[self.y]))

                    if event.type == pygame.QUIT:
                        self.running = False
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    PiratesGame().run()
