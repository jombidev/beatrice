import pygame

from src.gui.guiactions import Clickable, Drawable, Typeable
from src.utility.drawutil import DrawUtil
from src.utility.fontfactory import FontFactory, FontType
from src.utility.timestamp import get_system_time


class Input(Drawable, Clickable, Typeable):
    def __init__(self, placeholder: str, x: float, y: float, width: float = 200, height: float = 40, size: int = 24):
        self.placeholder = placeholder
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.value = ''
        self.focused = False
        self.size = size
        self.tick = get_system_time() + 1000
        self.key_repeat = []

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        width, height = FontFactory().font(FontType.ARIAL, self.size).size(self.value)
        DrawUtil().draw_box(self.x, self.y, self.width, self.height, color=0xff212121)
        for i, obj in enumerate(self.key_repeat):
            key, char, time = obj
            if get_system_time() - time > 200:
                self._key_consume(key, char)
                self.key_repeat[i] = (key, char, get_system_time() - 150)

        if not self.focused and len(self.value) == 0:
            DrawUtil().draw_string(self.placeholder, self.x + 5, self.y + self.height / 2 - height / 2, 0xffaaaaaa, size=self.size)
        else:
            if self.tick - get_system_time() < 0:
                self.tick = get_system_time() + 1000
            DrawUtil().draw_string(self.value, self.x + 5, self.y + self.height / 2 - height / 2, 0xffffffff, size=self.size)
            if self.tick - get_system_time() > 500 and self.focused:
                DrawUtil().draw_string('_', self.x + 5 + width, self.y + self.height / 2 - height / 2, 0xffffffff, size=self.size)

    def key_typed(self, key: int, char: str):
        if self.focused:
            self.tick = get_system_time() + 1000
            self.key_repeat.append((key, char, get_system_time()))
            self._key_consume(key, char)

    def _key_consume(self, key: int, char: str):
        if key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        elif key == pygame.K_RETURN:
            self.focused = False
            self.key_repeat.clear()
        else:
            self.value += char

    def key_released(self, key: int, char: str):
        for i, obj in enumerate(self.key_repeat):
            key, char, time = obj
            if key == key:
                del self.key_repeat[i]

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        if self._is_hovered(mouse_x, mouse_y):
            self.focused = True
            self.tick = get_system_time() + 1000
        else:
            self.focused = False

    def _is_hovered(self, mouse_x, mouse_y) -> bool:
        return DrawUtil().is_hovered(mouse_x, mouse_y, self.x, self.y, self.width, self.height)
