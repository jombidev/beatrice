from src.gui.guiactions import Drawable, Clickable, Typeable
from src.gui.screen.overlay import Input
from src.gui.screen.overlay import Slider
from src.static.constants import Constants


class Screen(Drawable, Clickable, Typeable):
    def __init__(self):
        self.overlays = []
        self.game = Constants().get('game')

    def init_screen(self):
        pass

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        if self.overlays:
            for btn in self.overlays:
                btn.draw_screen(mouse_x, mouse_y, partial_ticks)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        if self.overlays:
            for btn in self.overlays:
                btn.mouse_clicked(mouse_x, mouse_y, mouse_button)

    def mouse_released(self, mouse_x: int, mouse_y: int, mouse_button: int):
        if self.overlays:
            for sldr in self.overlays:
                if isinstance(sldr, Slider):
                    sldr.mouse_released(mouse_x, mouse_y, mouse_button)

    def key_typed(self, key: int, char: str):
        if self.overlays:
            for input in self.overlays:
                if isinstance(input, Input):
                    input.key_typed(key, char)

    def key_released(self, key: int, char: str):
        if self.overlays:
            for input in self.overlays:
                if isinstance(input, Input):
                    input.key_released(key, char)