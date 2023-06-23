from src.gui.guiactions import Drawable, Clickable, Typeable
from src.static.constants import Constants


class Screen(Drawable, Clickable, Typeable):
    def __init__(self):
        self.__buttons = []
        self.__sliders = []
        self.game = Constants().get('game')

    def init_screen(self):
        pass

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        if self.__buttons:
            for btn in self.__buttons:
                btn.draw_screen(mouse_x, mouse_y, partial_ticks)
        if self.__sliders:
            for sldr in self.__sliders:
                sldr.draw_screen(mouse_x, mouse_y, partial_ticks)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        if self.__buttons:
            for btn in self.__buttons:
                btn.mouse_clicked(mouse_x, mouse_y, mouse_button)
        if self.__sliders:
            for sldr in self.__sliders:
                sldr.mouse_clicked(mouse_x, mouse_y, mouse_button)

    def mouse_released(self, mouse_x: int, mouse_y: int, mouse_button: int):
        if self.__sliders:
            for sldr in self.__sliders:
                sldr.mouse_released(mouse_x, mouse_y, mouse_button)