from enum import Enum

import pygame.font


class FontType(Enum):
    ARIAL = 0
    TAHOMA = 1
    CALIBRI = 2
    CALIBRIBOLD = 3
    NANUM = 4

class FontFactory:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    __fonts = [[None for _ in range(128)] for _ in range(len(FontType))]

    def font(self, font: FontType, size: int = 16) -> pygame.font.FontType:
        if self.__fonts[font.value][size] is None:
            self.__fonts[font.value][size] = pygame.font.Font('resources/font/' + font.name.lower() + '.ttf', size)
        return self.__fonts[font.value][size]