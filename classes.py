import circuits

class Drawable:
    def draw(self, surface):
        pass

class Updatable (circuits.Component):
    def update(self, event):
        pass
