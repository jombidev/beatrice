from src.screen.button import Button
from src.screen.screen import Screen


class SettingScreen(Screen):
    def __init__(self, parent: Screen):
        super().__init__()
        self.parent = parent

    __buttons = []

    def __back(self):
        self.game.set_screen(self.parent)

    def init_screen(self):
        self.__buttons.append(Button("Back", 10, 10, False, self.__back, size=18))

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        for b in self.__buttons:
            b.draw_screen(mouse_x, mouse_y, partial_ticks)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        for b in self.__buttons:
            b.mouse_clicked(mouse_x, mouse_y, mouse_button)