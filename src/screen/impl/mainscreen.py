from src.screen.button import Button
from src.screen.impl.musics import MusicSelectScreen
from src.screen.screen import Screen
from src.utility.drawutil import DrawUtil


class MainScreen(Screen):
    def test_button_action(self):
        self.game.set_screen(MusicSelectScreen())

    def __exit_game(self):
        del self.game

    __buttons = []

    def init_screen(self):
        targetY = 720 - 80 * 5
        self.__buttons.append(Button("start", 1280 / 2, targetY, self.test_button_action))
        self.__buttons.append(Button("exit", 1280 / 2, targetY + 80, self.__exit_game))

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        for btn in self.__buttons:
            btn.draw_screen(mouse_x, mouse_y, partial_ticks)
        DrawUtil().draw_centered_string("Beatrice", 1280 / 2, 80, color=0xffffffff, size=48)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        for btn in self.__buttons:
            btn.mouse_clicked(mouse_x, mouse_y, mouse_button)

    def mouse_released(self, mouse_x: int, mouse_y: int, mouse_button: int):
        for btn in self.__buttons:
            btn.mouse_released(mouse_x, mouse_y, mouse_button)

    def key_typed(self, key: int, char: str):
        super().key_typed(key, char)
        print('typed', key, char)