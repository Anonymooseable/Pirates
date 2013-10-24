import circuits

class Update (circuits.Event):
    """Update Event"""

class KeyEvent (circuits.Event):
    """Generic Key event"""

class KeyDown (KeyEvent):
    """KeyDown Event"""

class KeyUp (KeyEvent):
    """KeyUp Event"""

class QuitRequest (circuits.Event):
    """User requested quit (pressing escape, closing window...)"""

class KeyHandler (circuits.Component):
    keydown_handlers = {}
    def key_down(self, event, pygame_event):
        if pygame_event.key in self.keydown_handlers:
            self.keydown_handlers[pygame_event.key](self)
    def key_up(self, event):
        pass
