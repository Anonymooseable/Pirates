import circuits

class Drawable (circuits.BaseComponent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.draw_channel = kwargs.get("order", 50)

	@handler("draw")
	def _on_draw(self, surface):
		pass

class Draw (circuits.Event):
	"""Event fired by the DrawManager to draw the components in its subtree."""

class DrawManager (circuits.BaseComponent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.channels = set()

	@handler("registered")
	def _on_registered(self, component, manager):
		print ("DrawManager:", component, "registered with", manager)
		if isinstance(component, Drawable):
			print ("It's drawable! Let's add it to our queue.")
			self.channels.add(component.channel)

	@handler("draw")
	def _on_draw(self, event, surface):
		for channel in sorted(self.channels):
			self.call(Draw(), channel)

class DrawGroup (list, Drawable):
	@handler("draw")
	def _on_draw(self, surface):
		for i in self:
			i.draw(surface)
