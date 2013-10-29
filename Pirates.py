#!/usr/bin/env python3

import pygame
import pygame as pg
import random
class PiratesGame:
    def __init__(self):
        pygame.init()
        self.clock=pygame.time.Clock()
        #Images--------------------------
        self.screen = pygame.display.set_mode((600, 600))#Creating a display creates a default surface: here we called it screen.(remember: 25px on sides, 20px between squares, 75px per square and half a square=37px

        pygame.display.set_caption('Yarrrr!!')

        self.cursor = pygame.image.load("Cross hair.png").convert_alpha()

        self.box_image = pygame.image.load("box.png").convert_alpha()

        self.board_background_image = pygame.image.load("board.png").convert_alpha()

        self.parch = pygame.image.load("parchment_75%.png").convert_alpha()

        self.splash = pygame.image.load("splash.png").convert_alpha()

        self.board_image = pygame.Surface(self.screen.get_size()).convert_alpha()

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
            self.state = "quit menu"
            self.old_state = "targeting"

        def fire(self):
            if self.board[self.x][self.y]==-1: # Empty square targeted: play splash animation
                for frame in range(0,35): # Animation has 35 frames
                    self.clock.tick(25) # Delay to ensure 25 FPS
                    rect=pygame.Rect(0+frame*75,0,75,75) # Region of the splash spritesheet to draw
                    self.screen.blit(self.board_image, (0, 0))
                    self.screen.blit(self.splash,(self.x_box[self.x],self.y_box[self.y]),rect)
                    self.screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
                    pygame.display.flip()
            else: # Square with a ship on it targeted: set its colour to orange (future: play ship hit animation)
                rect=pygame.Rect(self.x_box[self.x],self.y_box[self.y],75,75) # Get the square
                self.board_image.blit(self.board_background_image, (0,0))
                self.board_image.fill((240,150,75),rect) # Put orange on the board

        #Other---------------------------
        self.key_handlers = {   # all commands
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up,
            pg.K_ESCAPE: escape,
            pg.K_RETURN: fire
        }
        self.x_box = [25,120,215,310,405,500] # Distance of the left border of each box from the left of the screen
        self.y_box = [25,120,215,310,405,500] # Distance of the top border of each box from the top of the screen
        self.board = [[-1 for y in range(6)] for x in range(6)] # Create a 6x6 board filled with -1s

        #Generating ship positions
        # Notes for board contents:
        # -1 = Square free
        # >= 0 = Ship here
        for ship_id, ship_length in enumerate([2, 3, 3, 4]): # For each ship
            generated = False
            while not generated: # Attempt to place the ship until we are successful
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
        self.board_image.blit(self.board_background_image, (0, 0)) # First put in the background
        for x, x_pixels in enumerate(self.x_box):
            for y, y_pixels in enumerate(self.y_box):
                rect=pygame.Rect(x_pixels,y_pixels,75,75)#(x,y,width,height)
                if self.board[x][y] == -1: # If the square is free, draw it blue
                    self.board_image.blit(self.box_image,(x_pixels,y_pixels))
                else: # Otherwise some shade of grey depending on which ship is there
                    c = pygame.Color(0, 0, 0)
                    value = min(25 + 12*self.board[x][y], 100) # Value between 0 and 100
                    c.hsva = (0, 0, value, 100)
                    self.board_image.fill(c,rect)

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
        self.main_menu_image.blit(self.board_background_image, (0,0))
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
        self.quit_menu_image.blit(self.background_image, (0,0))
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        self.quit_menu_image.blit(self.quit_menu_really, (center_horiz_pos(self.quit_menu_really), self.menu_item_heights[0]))
        self.quit_menu_image.blit(self.quit_menu_yes, (center_horiz_pos(self.quit_menu_yes), self.menu_item_heights[1]))
        self.quit_menu_image.blit(self.quit_menu_no, (center_horiz_pos(self.quit_menu_no), self.menu_item_heights[2]))

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(25)
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

                    if event.type == pygame.QUIT:
                        self.running = False
                self.screen.blit(self.board_image,(0,0))
                self.screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
                self.screen.blit(self.cursor,(self.x_box[self.x],self.y_box[self.y]))

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    PiratesGame().run()
