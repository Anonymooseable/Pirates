#!/usr/bin/env python3

import circuits

import pygame
import pygame as pg

import grid
import ship

class Update (circuits.Event):
    """Update Event"""

class Draw (circuits.Event):
    """Draw Event"""

class KeyEvent (circuits.Event):
    """Generic Key event"""

class KeyDown (KeyEvent):
    """KeyDown Event"""

class KeyUp (KeyEvent):
    """KeyUp Event"""

class QuitRequest (circuits.Event):
    """User requested quit (pressing escape, closing window...)"""

class SelectionConfirmed (circuits.Event):
    """Fired when the selection of a square is confirmed by the user"""
    def __init__(self, selection):
        super().__init__()
        self.selection = selection

class Drawable:
    def draw(self):
        pass

class Updatable (circuits.Component):
    def update(self, *args):
        pass

class KeyHandler (circuits.Component):
    keydown_handlers = {}
    def key_down(self, event, pygame_event):
        if pygame_event.key in self.keydown_handlers:
            self.keydown_handlers[pygame_event.key](self)
    def key_up(self, event):
        pass

class State (Drawable, Updatable, KeyHandler):
    pass

class SelectingSquareState (State):
    def __init__(self):
        super().__init__()
        self.cursor_x = 0
        self.cursor_y = 0

    def update_cursor(self): # Updates the coordinates of the cursor
        self.cursor_pixelpos = self.root.grid.squares_to_pixels((self.cursor_x, self.cursor_y), centred = True, round = True)

    def registered(self, *args):
        self.update_cursor()

    def left(self):
        if self.cursor_x != 0:
            self.cursor_x -= 1
            self.update_cursor()

    def right(self):
        if self.cursor_x != self.parent.grid.width - 1:
            self.cursor_x += 1
            self.update_cursor()

    def down(self):
        if self.cursor_y != self.parent.grid.height - 1:
            self.cursor_y += 1
            self.update_cursor()

    def up(self):
        if self.cursor_y != 0:
            self.cursor_y -= 1
            self.update_cursor()

    def enter(self):
        self.fire(SelectionConfirmed((self.cursor_x, self.cursor_y)))
        self.unregister()

    keydown_handlers = {
        pg.K_LEFT: left,
        pg.K_RIGHT: right,
        pg.K_DOWN: down,
        pg.K_UP: up,
        pg.K_RETURN: enter
    }

    def draw(self):
        super().draw()
        pygame.draw.circle(self.parent.screen, (255, 0, 0), self.cursor_pixelpos, 10) # Draw cursor as a red circle

class PiratesGame (circuits.Component):
    FPS = 60
    def __init__(self):
        super().__init__()
        self.grid = grid.Grid(6, 6)
        self.state = SelectingSquareState().register(self)
        self.timer = circuits.Timer(1/self.FPS, Update(), persist = True).register(self)

        self.draw_queue = {10: self.state}

    def started(self, *args):
        pygame.init()
        self.screen = pygame.display.set_mode((self.grid.total_width, self.grid.total_height))
        pygame.display.set_caption('Yarrrr!!')

    def update(self, *args):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                e = KeyDown(event)
                self.fire(e)
            elif event.type == pygame.QUIT:
                self.fire(QuitRequest())
        self.draw()

    def draw(self, *args):
        self.grid.draw(self.screen)
        for key in sorted(self.draw_queue):
            self.draw_queue[key].draw()
        pygame.display.flip()

    def key_down(self, event, pygame_event):
        if pygame_event.key == pg.K_ESCAPE:
            self.fire(QuitRequest())

    def quit_request(self):
        self.stop()

    def confirmed_selection(self, event):
        print ("Selection confirmed:", event.selection)

    def prepare_unregister(self, event, component):
        pop_keys = []
        for key, value in self.draw_queue.items():
            print ("Checking whether to remove", value, "from draw queue")
            if event.in_subtree(value):
                pop_keys.append(key)
        for key in pop_keys:
            self.draw_queue.pop(key)

if __name__ == "__main__":
    PiratesGame().run()
