#!/usr/bin/env python3
"""
Quelques explications...

- pygame est une bibliothèque qui permet de créer des fenêtres et de dessiner dedans (ainsi que de faire des saisies)
- Tout ce qui concerne le dessin marche avec des surfaces: c'est des images numériques, des ensembles rectangulaires de pixels. On peut les créer vide, ou en chargeant une image, ou bien à partir d'une chaîne de caractères, en utilisant une police...
- L'écran (le contenu de la fenêtre) est aussi représenté par une surface. Les dessins qu'on fait dessus sont stockés, et le contenu n'est affiché que lorsqu'on appelle la fonction pygame.display.flip(). On peut s'imaginer que l'on dessine sur la face arrière de l'écran et que l'on le retourne avec la fonction flip()...
- On peut copier le contenu d'une surface sur une autre: ce processus s'appelle "blit" et on s'en servira beaucoup!
- Les saisies sont faites sous forme d'événements: on demande a pygame s'il y en a, puis on les traite un par un.
- Ceci se fait dans la boucle principale du jeu, ce qui donne un processus ressemblant à cela:
    1. Traiter les événements
    2. Avancer la logique du jeu
    3. Tout dessiner
    4. Afficher
Ce cycle se répète à une fréquence définie, que l'on appelle la fréquence d'images. Dans les jeux plus complexes, on cherche généralement à avoir une fréquence d'images de 60 images par seconde à peu près pour donner une impression de mouvement fluide.
Nous nous contentons de 25 images par seconde, car l'animation présente dans notre jeu est assez simple.

On maintient l'état du jeu dans un objet. Celui-ci comporte de diverses variables, par exemple:
- L'état général - si on est dans un menu et si oui lequel, ou bien dans le jeu lui-même
- La position du curseur, que ce soit celui représentant le choix dans le menu ou celui marquant la case visée par le joueur
- L'écran et d'autres surfaces (images, textes, table de jeu)

Passons au code!
"""

import random

import pygame
import pygame as pg

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

        # Animation pour les tirs ratés
        self.splash = pygame.image.load("splash.png").convert_alpha()

        # Surface où l'on dessinera tout ce qui ne bouge pas
        self.board_surface = pygame.Surface(self.screen.get_size()).convert()

        self.x = 0 # Position du curseur en abscisses
        self.y = 0 # Position du curseur en ordonnées

        self.x_box = [25,120,215,310,405,500] # Position du bord de gauche des six cases (distance du bord de gauche de la fenêtre)
        self.y_box = [25,120,215,310,405,500] # Position du bord supérieur des cases (distance du bord supérieur de la fenêtre)

        # Chargement des polices
        self.menu_item_heights = [60, 180, 270, 360, 450] # Espacement des éléments des menus (premier élément à 60px du bord supérieur, etc.)
        self.title_font = pygame.font.Font("Jean Lafitte.ttf", 50) # Police pour les titres des menus
        self.menu_font = pygame.font.Font("Primitive.ttf", 45) # Pour les éléments du menus
        self.shots_font = pygame.font.Font("Primitive.ttf", 25) # Et pour l'affichage du nombre de tirs restant
        def menu_title_text(text): # Fonction qui crée une surface contenant le texte donné avec lissage (True) en blanc (255, 255, 255)
            return self.title_font.render(text, True, (255, 255, 255))
        # Créer des titres divers pour les menus différents
        self.main_menu_title = menu_title_text("AHOY")
        self.pause_menu_title = menu_title_text("PAUSED")
        self.end_fail = menu_title_text("YER GOIN")
        self.end_fail_xtra = menu_title_text("DOWN")
        self.end_fail_xtra_xtra = menu_title_text("IN BUBBLES")
        self.end_win = menu_title_text("PLUNDERED")
        def menu_text(text): # Comme la fonction qui rend un titre, mais avec une autre police
            return self.menu_font.render(text, True, (255, 255, 255))
        self.menu_select_marker = menu_text(">") # Marqueur qui indiquera le choix actuel du joueur

        self.main_menu_image = pygame.Surface(self.screen.get_size()) # Surface qui contiendra le menu principal
        # Et maintenant, aux éléments du menu principal...

        self.main_menu_start = menu_text("Load the cannons!")

        # Élément du menu qui indique la difficulté choisie
        self.main_menu_easy = menu_text("Pansy >")
        self.main_menu_medium = menu_text("< Buff >")
        self.main_menu_hard = menu_text("< Cutthroat")

        self.main_menu_quit = menu_text("Flee")
        self.main_menu_sel = 0 # Position du curseur dans le menu principal
        self.main_menu_difficulty = 0 # 0 = facile, 1 = moyen, 2 = difficile
        self.difficulties = [25, 20, 15] # On a le droit à 25 tirs en mode facile, à 20 en mode moyen et à 15 en difficile

        self.pause_menu_image = pygame.Surface(self.screen.get_size()) # Surface qui contiendra le menu de pause
        self.pause_menu_resume = menu_text("Back to the fight!")
        self.pause_menu_main = menu_text("Come about again")
        self.pause_menu_exit = menu_text("Flee")
        self.pause_menu_sel = 0 # Position du curseur menu dans le menu de pause

        self.end_screen = pygame.Surface(self.screen.get_size()) # Surface qui contient le menu de fin de jeu (qui permet de repasser au menu principal ou de quitter)
        self.end_retry = menu_text("Come about again!")
        self.end_exit_win = menu_text("Grab yer Booty")
        self.end_exit_win_xtra = menu_text("and run!")
        self.end_exit_fail = menu_text("Surrender")
        self.end_screen_sel = 0 # Position du curseur menu dans le menu de fin de jeu

        self.running = False
        self.state = "main menu"
        # Créer les menus
        self.redraw_main_menu()
        self.draw_pause_menu()
    #------------------------------Fin de l'initialisation----------------------------#

    #------------------------Fonctions de dessin et de génération---------------------#

    def shots(self): # Dessine le nombre de tirs restant
        def shots_text(text):
            return self.shots_font.render(text, True, (255, 255, 255))
        shots_drawn = shots_text(str(self.shots_remaining))
        self.screen.blit(shots_drawn,(10,10))

    def redraw_main_menu(self): # Fonction qui redessine le menu principal
        self.main_menu_image.fill((0, 0, 0))
        self.main_menu_image.blit(self.background, (0,0)) # D'abord, mettre le fond d'écran
        self.main_menu_image.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT) # Ensuite la texture de parchement (elle ne va pas très bien en-dessus du texte)

        def center_horiz_pos(item): # Donne la position en abscisse pour centrer un élément
            return int(self.screen.get_width() / 2 - item.get_width() / 2)

        # Et on copie tous les éléments sur le menu
        self.main_menu_image.blit(self.main_menu_title, (center_horiz_pos(self.main_menu_title), self.menu_item_heights[0]))
        self.main_menu_image.blit(self.main_menu_start, (center_horiz_pos(self.main_menu_start), self.menu_item_heights[1]))
        if self.main_menu_difficulty == 0: # Choisir le bon pour la difficulté
            difficulty_image = self.main_menu_easy
        elif self.main_menu_difficulty == 1:
            difficulty_image = self.main_menu_medium
        elif self.main_menu_difficulty == 2:
            difficulty_image = self.main_menu_hard
        self.main_menu_image.blit(difficulty_image, (center_horiz_pos(difficulty_image), self.menu_item_heights[2]))
        self.main_menu_image.blit(self.main_menu_quit, (center_horiz_pos(self.main_menu_quit), self.menu_item_heights[3]))

    def draw_pause_menu(self): # Fonction qui dessine le menu de pause (comme le menu principal mais plus simple)
        self.pause_menu_image.fill((0, 0, 0))
        self.pause_menu_image.blit(self.background, (0,0))
        self.pause_menu_image.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        self.pause_menu_image.blit(self.pause_menu_title, (center_horiz_pos(self.pause_menu_title), self.menu_item_heights[0]))
        self.pause_menu_image.blit(self.pause_menu_resume, (center_horiz_pos(self.pause_menu_resume), self.menu_item_heights[1]))
        self.pause_menu_image.blit(self.pause_menu_main, (center_horiz_pos(self.pause_menu_main), self.menu_item_heights[2]))
        self.pause_menu_image.blit(self.pause_menu_exit, (center_horiz_pos(self.pause_menu_exit), self.menu_item_heights[3]))

    def draw_end_screen(self): # Fonction qui dessine le menu affiché à la fin du jeu
        self.end_screen.fill((0, 0, 0))
        self.end_screen.blit(self.background, (0,0))
        self.end_screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT)
        def center_horiz_pos(item):
            return int(self.screen.get_width() / 2 - item.get_width() / 2)
        if self.state == "player won": # Afficher les bons éléments en fonction de l'état de jeu (si le joueur a gagné ou perdu)
            self.end_screen.blit(self.end_win, (center_horiz_pos(self.end_win), self.menu_item_heights[0]))
            self.end_screen.blit(self.end_exit_win, (center_horiz_pos(self.end_exit_win), self.menu_item_heights[2]))
            self.end_screen.blit(self.end_exit_win_xtra, (center_horiz_pos(self.end_exit_win_xtra), self.menu_item_heights[2]+55))
            self.end_screen.blit(self.end_retry, (center_horiz_pos(self.end_retry), self.menu_item_heights[1]))
        if self.state == "player lost":
            self.end_screen.blit(self.end_fail, (center_horiz_pos(self.end_fail), self.menu_item_heights[0]))
            self.end_screen.blit(self.end_fail_xtra, (center_horiz_pos(self.end_fail_xtra), self.menu_item_heights[0]+60))
            self.end_screen.blit(self.end_fail_xtra_xtra, (center_horiz_pos(self.end_fail_xtra_xtra), self.menu_item_heights[0]+120))
            self.end_screen.blit(self.end_retry, (center_horiz_pos(self.end_retry), self.menu_item_heights[2]))
            self.end_screen.blit(self.end_exit_fail, (center_horiz_pos(self.end_exit_fail), self.menu_item_heights[3]))

    def generate_ships(self): # Fonction qui génère les bateaux et dessine les éléments statiques
        self.board = [[-1 for y in range(6)] for x in range(6)] # Créer la plage de jeu - 6x6 cases, remplies avec des -1

        # Signifiance des valeurs numériques des cases:
        # -2 = Case libre, le joueur a déjà tiré dessus
        # -1 = Case libre
        # >= 0 mais < 20 = Bateau
        # > 20 = Bateau endommagé

        # Placement des bateaux (aléatoire)
        for ship_id, ship_length in enumerate([2, 3, 3, 4]): # Pour chaque bateau (longueurs: 1x2, 2x3, 1x4)
            generated = False
            while not generated: # On refait des coordonnées aléatoires jusqu'à ce qu'on réussit à placer le bateau
                x_or_y=random.choice(('horizontal','vertical')) # Choisir de façon aléatoire l'orientation du bateau
                if x_or_y == 'horizontal': # Si le bateau est horizontal, on modifiera l'abscisse pour avoir toutes les cases
                    ship_posx=random.randint(0,5-ship_length) # Abscisse = entier aléatoire entre 0 et (5-longueur) (pour que le bateau puisse s'étendre vers la droite)
                    ship_posy=random.randint(0,5) # Ordonnée = entier aléatoire entre 0 et 5
                    generated = True # Tout va bien jusque là, maintenant on va tester s'il n'y a pas de collision
                    for position_on_ship in range(0, ship_length): # position_on_ship = la distance de l'"origine" du bateau
                        x = ship_posx + position_on_ship # Abscisse de la case qu'on teste
                        if self.board[x][ship_posy] != -1: # Si la case n'est pas libre
                            generated = False # Alors on a échoué
                            break # Et on peut aller au prochain tout de suite.
                    if generated: # Mais si on a réussi à placer le bateau...
                        for position_on_ship in range(ship_length): # On passe de nouveau sur toutes les cases du bateau
                            x = ship_posx + position_on_ship
                            self.board[x][ship_posy] = ship_id # Et on marque la case comme occupée

                else: # De même pour les bateaux verticaux, mais on modifiera l'ordonnée
                    ship_posx=random.randint(0,5)
                    ship_posy=random.randint(0,5-ship_length)
                    generated = True
                    for position_on_ship in range(0, ship_length):
                        y = ship_posy + position_on_ship
                        if self.board[ship_posx][y] != -1:
                            generated = False
                    if generated:
                        for position_on_ship in range(ship_length):
                            y = ship_posy + position_on_ship
                            self.board[ship_posx][y] = ship_id

        # Enfin, tout dessiner
        self.board_surface.blit(self.background, (0, 0)) # Copier le fond d'écran
        for x, x_pixels in enumerate(self.x_box): # Pour toutes les rangées (abscisse en pixels de la case en self.x_box)
            for y, y_pixels in enumerate(self.y_box): # Et pour chaque case
                rect=pygame.Rect(x_pixels,y_pixels,75,75) # Le rectangle correspondant à la case (position en abscisses, position en ordonnées, longueur, largeur)
                self.board_surface.blit(self.box_image,(x_pixels,y_pixels)) # Copier l'image "case vide" (avec des vagues) sur la surface
#------------------------------- fin de la génération des bateaux

    #-----------Fonction qui contient le jeu en lui-même-----------#
    def run(self):
        self.running = True # On est en marche
        while self.running: # Tant qu'on l'est
            self.clock.tick(25) # Délai pour une fréquence d'images de 25
            if self.state == "main menu": # Si on est dans le menu principal
                for event in pygame.event.get(): # Traiter les événements (entrée de données)
                    if event.type == pygame.QUIT: # Le joueur a fermé la fenêtre
                        self.running = False # On quitte!
                    if event.type == pg.KEYDOWN: # On a appuyé sur une touche du clavier
                        if event.key == pg.K_UP:
                            self.main_menu_sel -= 1 # Déplacer le curseur vers le haut dans le menu
                            self.main_menu_sel %= 3 # Puis utiliser un modulo pour le faire passer à 2 s'il est à -1
                        elif event.key == pg.K_DOWN:
                            self.main_menu_sel += 1 # Déplacer vers le bas
                            self.main_menu_sel %= 3 # Modulo: 3 => 0
                        elif event.key == pg.K_ESCAPE: # Si l'utilisateur appuie sur la touche échap
                            self.main_menu_sel = 2 # On met le curseur sur le 3eme élément du menu (quitter)
                        elif event.key == pg.K_RETURN: # L'utilisateur a confirmé
                            if self.main_menu_sel == 0: # Premier élément du menu: commencer le jeu
                                self.generate_ships() # On place les bateaux
                                self.shots_remaining = self.difficulties[self.main_menu_difficulty] # On initialise le nombre de tirs
                                self.state = "targeting" # Et on se met en état de jeu
                            elif self.main_menu_sel == 2: # Troisième élément du menu: quitter
                                self.running = False # Alors on quitte!
                        # Si le curseur est sur le 2ème élément du menu...
                        elif event.key == pg.K_LEFT and self.main_menu_sel == 1 and self.main_menu_difficulty > 0: # Gauche = baisser la difficulté si possible
                            self.main_menu_difficulty -= 1
                            self.redraw_main_menu() # Et on redessine le menu principal pour prendre en compte le changement d'un de ses éléments
                        elif event.key == pg.K_RIGHT and self.main_menu_sel == 1 and self.main_menu_difficulty < 2: # Droite = l'augmenter
                            self.main_menu_difficulty += 1
                            self.redraw_main_menu()
                # Et on dessine le menu principal
                self.screen.blit(self.main_menu_image, (0, 0))
                # Et le marqueur qui indique la sélection
                self.screen.blit(self.menu_select_marker, (10, self.menu_item_heights[self.main_menu_sel+1])) # (à 10px du bord de gauche de la fenêtre, et aligné avec l'élément choisi)

            elif self.state == "pause menu": # Comme le menu principal mais plus simple
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            self.pause_menu_sel -= 1
                            self.pause_menu_sel %= 3
                        elif event.key == pg.K_DOWN:
                            self.pause_menu_sel += 1
                            self.pause_menu_sel %= 3
                        elif event.key == pg.K_RETURN:
                            if self.pause_menu_sel == 0: # Continuer
                                self.state = "targeting"
                            elif self.pause_menu_sel == 1: # Retour au menu principal
                                self.state = "main menu"
                            elif self.pause_menu_sel == 2: # Quitter
                                self.running = False
                self.screen.blit(self.pause_menu_image, (0, 0))
                cursor_height = self.menu_item_heights[self.pause_menu_sel + 1]
                self.screen.blit(self.menu_select_marker, (10, cursor_height))

            elif self.state == "targeting": # On est en train de jouer
                for event in pygame.event.get():
                    if event.type==pg.KEYDOWN: # Si on a appuyé sur une touche
                        if event.key == pg.K_LEFT: # Si la touche est la touche "gauche"
                            if self.x != 0: # Et si le curseur n'est pas déjà tout à gauche...
                                self.x -= 1 # On le déplace vers la gauche
                        elif event.key ==pg.K_RIGHT: # idem, droite
                            if self.x != 5:
                                self.x += 1
                        elif event.key ==pg.K_DOWN: # idem, vers le bas
                            if self.y != 5:
                                self.y += 1
                        elif event.key ==pg.K_UP: # idem, vers le haut
                            if self.y!=0:
                                self.y -= 1
                        elif event.key ==pg.K_ESCAPE: # Passer en état "menu de pause"
                            self.state = "pause menu"
                            self.old_state = "targeting"

                        elif event.key ==pg.K_RETURN: # Tirer sur une case
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

                    if event.type == pygame.QUIT: # Quitter si l'utilisateur ferme la fenêtre
                        self.running = False
                self.screen.blit(self.board_surface,(0,0)) # Dessiner le "terrain de jeu"
                self.screen.blit(self.parch,(0,0),None,pg.BLEND_RGBA_MULT) # Et le parchement par-dessus
                self.shots() # Puis le nombre de tirs restant
                self.screen.blit(self.cursor,(self.x_box[self.x],self.y_box[self.y])) # Et le curseur.

            elif self.state == "player won" or self.state == "player lost": # Fin du jeu: dessiner le menu (comme les menus principal et de pause)
                if self.exit_screen_draw:
                    self.draw_end_screen() # Redessiner le menu de fin de jeu si nécessaire
                    self.exit_screen_draw = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
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

            pygame.display.flip() # Et tout afficher
        pygame.quit()


if __name__ == "__main__":
    PiratesGame().run()
