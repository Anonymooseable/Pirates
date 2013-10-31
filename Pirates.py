#!/usr/bin/env python3

import pygame
import pygame as pg
import random

# Classe qui maintient l'état du jeu
class PiratesGame:
    def __init__(self): # Fonction appelée lors de la création d'un PiratesGame
        pygame.init() # Initialiser pygame pour que tout fonctionne
        self.clock=pygame.time.Clock() # Créer une Clock qui gère la synchronisation
        # Créer une fenêtre et la stocker dans l'attribut de la classe "screen" (taille 600x600 pixels)
        self.screen = pygame.display.set_mode((600, 600))
        # Espacement:
        #  - 25px de marge sur les 4 bords de la fenêtre
        #  - 20px entre toutes les cases
        #  - Chaque case = 75x75px

        pygame.display.set_caption('Yarrrr!!') # Définir le titre de la fenêtre

        #Images--------------------------

        # pygame.image.load("nom de fichier") charge une image, et convert_alpha() la convertit dans un format qui est adapté pour l'afficher à l'écran avec sa transparence (ou, si on n'a pas besoin de transparence, on utilisera convert())
        # Curseur qui marque la case sélectionnée
        self.cursor = pygame.image.load("Cross hair.png").convert_alpha()

        # Image pour une case vide/non découverte
        self.box_image = pygame.image.load("box.png").convert_alpha()

        # Fond d'écran
        self.background = pygame.image.load("board.png").convert()

        # Texture de parchemin pour mettre en-dessus
        self.parch = pygame.image.load("parchment.png").convert_alpha()

        # Animation: plouf!
        self.splash = pygame.image.load("splash.png").convert_alpha()

        # Surface (ensemble rectangulaire de pixels) où l'on dessinera tout ce qui ne bouge pas
        self.board_surface = pygame.Surface(self.screen.get_size()).convert()

        self.x = 0 # Position du curseur en abscisses
        self.y = 0 # Position du curseur en ordonnées

        # Fonctions réagissant aux touches de clavier
        def left(self): # Déplacer le curseur vers la gauche
            if self.x != 0: # Mais seulement s'il n'est pas déjà tout à gauche
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
        def escape(self): # Mettre le jeu en pause
            self.state = "pause menu"
            self.old_state = "targeting"

        def fire(self): # Tirer sur une case (dont les coordonnées seront déterminées par self.x et self.y, les coordonnées du curseur)
            if self.board[self.x][self.y] in (-1,-2): # La case est vide: plouf!
                self.board[self.x][self.y] = -2 # Indiquer qu'on a déjà tiré sur cette case
                for frame in range(0,35): # L'animation comporte 35 images
                    self.clock.tick(25) # On attend pour assurer une fréquence d'image maximale de 25 images/seconde
                    rect=pygame.Rect(0+frame*75,0,75,75) # On détermine quelle image on veut dessiner (quelle région du fichier)
                    self.screen.blit(self.board_surface, (0, 0)) # Copier l'image statique sur l'écran
                    self.screen.blit(self.splash,(self.x_box[self.x],self.y_box[self.y]),rect) # Copier l'image actuelle de l'animation, à la bonne position
                    self.screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT) # Copier la texture de parchemin par-dessus
                    self.shots()# Dessiner le nombre de tirs qui restent
                    pygame.display.flip() # Et afficher le tout
            elif self.board[self.x][self.y] < 20: # Il y a un bateau sur la case!
                rect=pygame.Rect(self.x_box[self.x],self.y_box[self.y],75,75) # On détermine les coordonnées du carré
                self.board_surface.fill((240,150,75),rect) # Remplir ce carré en orange sur l'image statique
                self.board[self.x][self.y] += 20 # Marquer que le bateau qui y est situé est endommagé

                player_won = True
                for row in self.board:
                    for square in row: # Ensuite on regarde sur toutes les cases pour voir s'il reste des bateaux ennemis
                        if 0 <= square < 20: # Et s'il y en a...
                            player_won = False # Le joueur n'a pas gagné
                            break # Et on peut sortir de la boucle tout de suite.
                if player_won: # Ensuite si le joueur a gagné...
                    self.state = "player won" # On se met dans l'état de jeu "player won" (où l'on affiche un menu pour recommencer ou pour quitter le jeu)
                    self.exit_screen_draw = True #################################################
                    return # On évite de déterminer si le joueur a perdu en sortant tout de suite de la fonction
            # Et si la valeur de la case est supérieure à 20, le joueur a tiré sur une case où il avait déjà touché un bateau, et gaspillé un tir... Tant pis pour lui!
            # Dans tous les cas, on soustrait 1 au nombre de tirs restant.
            self.shots_remaining -= 1
            if self.shots_remaining <= 0: # Et si le joueur n'en a plus...
                self.state = "player lost" # Le joueur a perdu...
                self.exit_screen_draw = True # Draw the screen the first time you end a game #########################

        self.key_handlers = { # Associer des touches du clavier aux fonctions qu'on vient de créer
            pg.K_LEFT: left,
            pg.K_RIGHT: right,
            pg.K_DOWN: down,
            pg.K_UP: up,
            pg.K_ESCAPE: escape,
            pg.K_RETURN: fire
        }
        self.x_box = [25,120,215,310,405,500] # Position du bord de gauche des six cases (distance du bord de gauche de la fenêtre)
        self.y_box = [25,120,215,310,405,500] # Position du bord supérieur des cases (distance du bord supérieur de la fenêtre)

        # Chargement des polices
        self.menu_item_heights = [60, 180, 270, 360, 450] # Espacement des éléments des menus (premier élément à 60px du bord supérieur, etc.)
        self.title_font = pygame.font.Font("Jean Lafitte.ttf", 50) # Police pour les titres des menus
        self.menu_font = pygame.font.Font("Primitive.ttf", 45) # Pour les éléments du menus
        self.shots_font = pygame.font.Font("Primitive.ttf", 25) # Et pour l'affichage du nombre de tirs restant
        def menu_title_text(text): # Fonction qui 
            return self.title_font.render(text, True, (255, 255, 255))
        self.main_menu_title = menu_title_text("AHOY")
        self.pause_menu_title = menu_title_text("PAUSED")
        self.end_fail = menu_title_text("YER GOIN")
        self.end_fail_xtra = menu_title_text("DOWN")
        self.end_fail_xtra_xtra = menu_title_text("IN BUBBLES")
        self.end_win = menu_title_text("PLUNDERED")
        def menu_text(text): # Function for rendering a menu item (to avoid copying True, (255, 255, 255) each time)
            return self.menu_font.render(text, True, (255, 255, 255))
        self.menu_select_marker = menu_text(">") # Marker for showing which item is currently selected

        self.main_menu_image = pygame.Surface(self.screen.get_size()) # Surface containing the rendered main menu
        self.main_menu_start = menu_text("Load the canons!")

        # Difficulty menu item
        self.main_menu_easy = menu_text("Pansy >")
        self.main_menu_medium = menu_text("< Buff >")
        self.main_menu_hard = menu_text("< Cutthroat")

        self.main_menu_quit = menu_text("Flee")
        self.main_menu_sel = 0 # Position of the cursor in the main menu
        self.main_menu_difficulty = 0 # 0 = easy, 1 = medium, 2 = hard
        self.difficulties = [25, 20, 15] # 30 shots in easy, etc; allows for 13, 8, and 3 misses respectively

        self.pause_menu_image = pygame.Surface(self.screen.get_size()) # Surface containing the rendered quit menu
        self.pause_menu_resume = menu_text("Back to the fight!")
        self.pause_menu_main = menu_text("Come about again")
        self.pause_menu_exit = menu_text("Flee")
        self.pause_menu_sel = 0 # Position of the cursor in the pause menu

        self.end_screen = pygame.Surface(self.screen.get_size()) # Surface containing the rendered end menu
        self.end_retry = menu_text("Come about again!")
        self.end_exit_win = menu_text("Grab yer Booty")
        self.end_exit_win_xtra = menu_text("and run!")
        self.end_exit_fail = menu_text("Surrender")
        self.end_screen_sel = 0 # Position of the cursor in the end menu
        
        self.running = False
        self.state = "main menu"
        self.redraw_main_menu() # Render the menus
        self.draw_pause_menu()
#------------------------------------------------------------------------------------------------------def __init__ ends here        
            #------------------------Drawing and generation functions---------------------#

    def shots(self): #Func that draws the shots remaining
        def shots_text(text): 
            return self.shots_font.render(text, True, (255, 255, 255))
        shots_drawn = shots_text(str(self.shots_remaining))
        self.screen.blit(shots_drawn,(10,10))
        
    def redraw_main_menu(self): # Function for drawing the main menu
        self.main_menu_image.fill((0, 0, 0))
        self.main_menu_image.blit(self.background, (0,0)) # Put in the background
        self.main_menu_image.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)

        def center_horiz_pos(item): # Returns the x position for centering a menu item horizontally
            return int(self.screen.get_width() / 2 - item.get_width() / 2)

        # Draw each menu item
        self.main_menu_image.blit(self.main_menu_title, (center_horiz_pos(self.main_menu_title), self.menu_item_heights[0]))
        self.main_menu_image.blit(self.main_menu_start, (center_horiz_pos(self.main_menu_start), self.menu_item_heights[1]))
        if self.main_menu_difficulty == 0:
            difficulty_image = self.main_menu_easy
        elif self.main_menu_difficulty == 1:
            difficulty_image = self.main_menu_medium
        elif self.main_menu_difficulty == 2:
            difficulty_image = self.main_menu_hard
        self.main_menu_image.blit(difficulty_image, (center_horiz_pos(difficulty_image), self.menu_item_heights[2]))
        self.main_menu_image.blit(self.main_menu_quit, (center_horiz_pos(self.main_menu_quit), self.menu_item_heights[3]))

    def draw_pause_menu(self): # Function for drawing the quit menu (similar to main menu drawing function)
        self.pause_menu_image.fill((0, 0, 0))
        self.pause_menu_image.blit(self.background, (0,0))
        self.pause_menu_image.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        self.pause_menu_image.blit(self.pause_menu_title, (center_horiz_pos(self.pause_menu_title), self.menu_item_heights[0]))
        self.pause_menu_image.blit(self.pause_menu_resume, (center_horiz_pos(self.pause_menu_resume), self.menu_item_heights[1]))
        self.pause_menu_image.blit(self.pause_menu_main, (center_horiz_pos(self.pause_menu_main), self.menu_item_heights[2]))
        self.pause_menu_image.blit(self.pause_menu_exit, (center_horiz_pos(self.pause_menu_exit), self.menu_item_heights[3]))
        
    def draw_end_screen(self): # Function for drawing the end screen menu (similar to main menu drawing function)
        self.end_screen.fill((0, 0, 0))
        self.end_screen.blit(self.background, (0,0))
        self.end_screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        if self.state == "player won":
            self.end_screen.blit(self.end_win, (center_horiz_pos(self.end_win), self.menu_item_heights[0]))
            self.end_screen.blit(self.end_exit_win, (center_horiz_pos(self.end_exit_win), self.menu_item_heights[2]))
            self.end_screen.blit(self.end_exit_win_xtra, (center_horiz_pos(self.end_exit_win_xtra), self.menu_item_heights[2]+55))
            self.end_screen.blit(self.end_retry, (center_horiz_pos(self.end_retry), self.menu_item_heights[1]))
        if self.state == "player lost":
            self.end_screen.blit(self.end_fail, (center_horiz_pos(self.end_fail), self.menu_item_heights[0]))
            self.end_screen.blit(self.end_fail_xtra, (center_horiz_pos(self.end_fail_xtra), self.menu_item_heights[0]+60))
            self.end_screen.blit(self.end_fail_xtra_xtra, (center_horiz_pos(self.end_fail_xtra_xtra), self.menu_item_heights[0]+120))
            self.end_screen.blit(self.end_exit_fail, (center_horiz_pos(self.end_exit_fail), self.menu_item_heights[3]))
            self.end_screen.blit(self.end_retry, (center_horiz_pos(self.end_retry), self.menu_item_heights[2]))
        
    def generate_ships(self):  #this actually generates the ship and draws the board
        self.board = [[-1 for y in range(6)] for x in range(6)] # Create a 6x6 board filled with -1s

        #Generating ship positions
        # Notes for board contents:
        # -1 = Square free
        # >= 0 but < 20 = Ship here
        # > 20 = ship, but has been hit
        for ship_id, ship_length in enumerate([2, 3, 3, 4]): # For each ship
            generated = False
            while not generated: # Attempt to place the ship until we are successful
                x_or_y=random.choice(('horizontal','vertical'))
                if x_or_y == 'horizontal':                  #code for generating horizontal ships
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

                else:                           #code for generating vertical ships
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
        self.board_surface.blit(self.background, (0, 0)) # First put in the background
        for x, x_pixels in enumerate(self.x_box):
            for y, y_pixels in enumerate(self.y_box):
                rect=pygame.Rect(x_pixels,y_pixels,75,75)#(x,y,width,height)
                if self.board[x][y] == -1: # If the square is free, draw it blue
                    self.board_surface.blit(self.box_image,(x_pixels,y_pixels))
                else: # Otherwise some shade of grey depending on which ship is there
                    c = pygame.Color(0, 0, 0)
                    value = min(25 + 12*self.board[x][y], 100) # Value between 0 and 100
                    c.hsva = (0, 0, value, 100)
                    self.board_surface.fill(c,rect)
#-------------------------------------------------------------------------------------------------------------------------def generate_ships ends here
           #-----------This is the core running functions that calls all the other functions (except the generation code)-----------#
    def run(self):
        self.running = True
        while self.running: # While the user hasn't confirmed that they want to quit
            self.clock.tick(25)
            if self.state == "main menu":
                for event in pygame.event.get(): # Handle events
                    if event.type == pygame.QUIT: #click on the x
                        self.running = False
                    if event.type == pg.KEYDOWN: # A key pas pressed
                        if event.key == pg.K_UP: # The key was the up key
                            self.main_menu_sel -= 1 # Move the cursor up in the menu
                            self.main_menu_sel %= 3 # Wrap to the bottom if it's out of bound
                        elif event.key == pg.K_DOWN:
                            self.main_menu_sel += 1 # Move it down
                            self.main_menu_sel %= 3
                        elif event.key == pg.K_ESCAPE: # Move the cursor to the "quit" item
                            self.main_menu_sel = 2
                        elif event.key == pg.K_RETURN: # Confirm a choice
                            if self.main_menu_sel == 0: # Start: set the state to targeting
                                self.generate_ships()
                                self.state = "targeting"
                                self.shots_remaining = self.difficulties[self.main_menu_difficulty]
                            elif self.main_menu_sel == 2:
                                self.running = False
                        # Increase/Decrease the difficulty if the cursor is on the second menu item (difficulty) and it's not already at the minimum/maximum
                        elif event.key == pg.K_LEFT and self.main_menu_sel == 1 and self.main_menu_difficulty > 0:
                            self.main_menu_difficulty -= 1
                            self.redraw_main_menu()
                        elif event.key == pg.K_RIGHT and self.main_menu_sel == 1 and self.main_menu_difficulty < 2:
                            self.main_menu_difficulty += 1
                            self.redraw_main_menu()
                # After handling events, draw the menu to the screen
                self.screen.blit(self.main_menu_image, (0, 0))
                # And the marker
                self.screen.blit(self.menu_select_marker, (10, self.menu_item_heights[self.main_menu_sel+1]))

            elif self.state == "pause menu": # Mostly like the main menu, just simpler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #click on the x
                        self.running = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            self.pause_menu_sel -= 1
                            self.pause_menu_sel %= 3
                        elif event.key == pg.K_DOWN:
                            self.pause_menu_sel += 1
                            self.pause_menu_sel %= 3
                        elif event.key == pg.K_RETURN:
                            if self.pause_menu_sel == 0:
                                self.state = "targeting"
                            elif self.pause_menu_sel == 1:
                                self.state = "main menu"
                            elif self.pause_menu_sel == 2:
                                self.running = False
                self.screen.blit(self.pause_menu_image, (0, 0))
                cursor_height = self.menu_item_heights[self.pause_menu_sel + 1]
                self.screen.blit(self.menu_select_marker, (10, cursor_height))

            elif self.state == "targeting": # Actually playing
                for event in pygame.event.get():
                    if event.type==pg.KEYDOWN and event.key in self.key_handlers:
                        self.key_handlers[event.key](self)

                    if event.type == pygame.QUIT:
                        self.running = False
                self.screen.blit(self.board_surface,(0,0))
                self.screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
                self.shots() #Run the func that draws the shots remaining
                self.screen.blit(self.cursor,(self.x_box[self.x],self.y_box[self.y]))

            elif self.state == "player won" or self.state == "player lost": #Game over and Victory screen
                if self.exit_screen_draw:    #Draw the screen the first time you end a game
                    self.draw_end_screen()  #Draw it again cause otherwise it's bugged (it didn't have the self.state before)
                    self.exit_screen_draw = False   # Now that it's drawn don't draw it a again
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #click on the x
                        self.running = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            self.end_screen_sel -= 1
                            self.end_screen_sel *= -1
                        elif event.key == pg.K_DOWN:
                            self.end_screen_sel += 1
                            self.end_screen_sel %= 2
                        elif event.key == pg.K_RETURN:
                            if self.end_screen_sel == 0:
                                self.state = "main menu"
                            elif self.end_screen_sel == 1:
                                self.running = False
                        elif event.key == pg.K_ESCAPE:
                            self.end_screen_sel = 1
                self.screen.blit(self.end_screen, (0, 0))
                if self.state == "player won":
                    cursor_height = self.menu_item_heights[self.end_screen_sel + 1]
                else:
                    cursor_height = self.menu_item_heights[self.end_screen_sel + 2]
                self.screen.blit(self.menu_select_marker, (10, cursor_height))

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    PiratesGame().run()
