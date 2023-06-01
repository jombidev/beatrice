import time

import pygame

from src.instances import Game, get_system_time
import os

from src.screen.impl.mainscreen import MainScreen
from src.static.constants import Constants

os.environ["MTL_HUD_ENABLED"] = "1"

prevTime = 0

if __name__ == '__main__':
    g = Game('testing', 1280, 720)
    Constants().set('game', g)
    running = True
    g.set_screen(MainScreen())
    while running:
        for ev in g.poll():
            if ev.type == pygame.QUIT:
                running = False
            if g.get_screen() is not None:
                if ev.type == pygame.KEYDOWN:
                    g.get_screen().key_typed(ev.key, ev.unicode)
                elif ev.type == pygame.MOUSEWHEEL:
                    g.get_screen().mouse_scrolled(*pygame.mouse.get_pos(), ev.x, ev.y)
        g.screen.fill('black')
        repeat = g.get_ticker().advance_time(get_system_time())
        for i in range(min(10, repeat)):
            Constants().add('tick', 1)
        g.update()
        g.flip()
        g.fixFrame(240)  # vsync
    del g
