import sys

import pygame
import time

from src.screen.screen import Screen


def get_system_time():
    return time.time_ns() / 1000000


class Game:
    def __init__(self, title: str, width: int, height: int):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticker = Timer(60.0)
        pygame.display.set_caption(title)

    __currentScreen = None
    __press = []

    def set_screen(self, screen: Screen):
        if screen is None:
            return
        self.__currentScreen = screen
        screen.init_screen()

    def clear_screen(self):
        self.__currentScreen = None

    def get_screen(self) -> Screen:
        return self.__currentScreen

    def poll(self):
        return [*pygame.event.get()]

    def get_ticker(self):
        return self.ticker

    def update(self):
        if self.__currentScreen is not None:
            x, y = pygame.mouse.get_pos()
            self.__currentScreen.draw_screen(x, y, self.ticker.partial_tick)

            for i, pressed in enumerate(pygame.mouse.get_pressed()):
                if pressed and i not in self.__press:
                    self.__press.append(i)
                    self.__currentScreen.mouse_clicked(x, y, i)
                if not pressed and i in self.__press:
                    self.__press.remove(i)
                    self.__currentScreen.mouse_released(x, y, i)

    def flip(self):
        pygame.display.flip()

    def fixFrame(self, fps: float):
        self.clock.tick(fps)

    def __del__(self):
        pygame.quit()
        sys.exit()


class Timer:
    def __init__(self, tps: float):
        self.tps = tps
        self.tick_delta = 0.0
        self.partial_tick = 0.0
        self.ms_per_tick = 1000.0 / tps
        self.last_ms = 0

    def advance_time(self, current_ms: int) -> int:
        self.tick_delta = float(current_ms - self.last_ms) / self.ms_per_tick
        self.last_ms = current_ms
        self.partial_tick += self.tick_delta
        tick_int = int(self.partial_tick)
        self.partial_tick -= tick_int
        return tick_int  # loop count