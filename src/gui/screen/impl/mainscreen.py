from src.gui.screen.impl.multi import MultiScreen
from src.gui.screen.util.button import Button
from src.gui.screen.impl.musics import MusicSelectScreen
from src.gui.screen.impl.setting import SettingScreen
from src.gui.screen.screen import Screen
from src.utility.drawutil import DrawUtil


class MainScreen(Screen):
    def __start_music_selection(self):
        self.game.set_screen(MultiScreen(self))

    def __setting(self):
        self.game.set_screen(SettingScreen(self))

    def __exit_game(self):
        self.game.__del__()

    def init_screen(self):
        self._Screen__buttons.clear()
        target_y = 720 - 80 * 5
        self._Screen__buttons.append(Button("start", 1280 / 2, target_y, None, None, True, self.__start_music_selection))
        self._Screen__buttons.append(Button("settings", 1280 / 2, target_y + 50, None, None, True, self.__setting))
        self._Screen__buttons.append(Button("exit", 1280 / 2, target_y + 100, None, None, True, self.__exit_game))

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        super().draw_screen(mouse_x, mouse_y, partial_ticks)
        DrawUtil().draw_centered_string("Beatrice", 1280 / 2, 80, color=0xffffffff, size=48)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        super().mouse_clicked(mouse_x, mouse_y, mouse_button)

    def key_typed(self, key: int, char: str):
        super().key_typed(key, char)
        print('typed', key, char)
