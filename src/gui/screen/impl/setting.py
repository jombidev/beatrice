import time

import pygame.mixer

from src.config import save_state, CONFIGS, load_states
from src.gui.screen.util.button import Button
from src.gui.screen.screen import Screen
from src.gui.screen.util.slider import Slider
from src.utility.drawutil import DrawUtil
from src.utility.fontfactory import FontType, FontFactory
from src.utility.soundutil import SoundUtil
from src.utility.timestamp import get_system_time


class SettingScreen(Screen):
    def __init__(self, parent: Screen):
        super().__init__()
        self.parent = parent

    __last_ms = get_system_time()

    def __back(self):
        self.game.set_screen(self.parent)

    def __listen(self, value: float):
        save_state('VOLUME', value)
        pygame.mixer.music.set_volume(value)
        if get_system_time() - self.__last_ms > 50:
            self.__last_ms = get_system_time()
            SoundUtil().play('resources/t.wav')

    def __offset_low(self):
        off = round((CONFIGS['OFFSET'] - 0.1) * 100) / 100
        save_state('OFFSET', off)

    def __offset_high(self):
        off = round((CONFIGS['OFFSET'] + 0.1) * 100) / 100
        save_state('OFFSET', off)

    def init_screen(self):
        self._Screen__buttons.clear()
        self._Screen__sliders.clear()
        load_states()
        self._Screen__buttons.append(Button("Back", 10, 10, None, None, False, self.__back, size=18))
        self._Screen__sliders.append(Slider('Volume', 50, 50, 200, 40, self.__listen, value=CONFIGS['VOLUME']))
        self._Screen__buttons.append(Button('<', 50, 100, None, None, False, self.__offset_low, size=18))
        self._Screen__buttons.append(Button('>', 220, 100, None, None, False, self.__offset_high, size=18))

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        super().draw_screen(mouse_x, mouse_y, partial_ticks)

        w, h = FontFactory().font(FontType.ARIAL, 18).size('>')
        width = w + 20
        DrawUtil().draw_centered_string(f'Offset: {CONFIGS["OFFSET"]}', 50 + (220 - 50 + width) / 2, 100 + h / 2 + 2, 0xffffffff)