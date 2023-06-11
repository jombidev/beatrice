from src.screen.guiactions import Drawable, Clickable, Typeable
from src.static.constants import Constants


class Screen(Drawable, Clickable, Typeable):
    def __init__(self):
        self.game = Constants().get('game')

    def init_screen(self):
        pass