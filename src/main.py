import pygame

from src.config import *
from src.instances import Game
import os

from src.gui.screen.impl.mainscreen import MainScreen
from src.static.constants import Constants
from src.utility.timestamp import *

import nest_asyncio
nest_asyncio.apply()

# os.environ["MTL_HUD_ENABLED"] = "1"

prevTime = 0

if __name__ == '__main__':
    if not os.path.exists('config.json'):
        save_states()
    load_states()

    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=64)
    g = Game('testing', 1280, 720)

    pygame.mixer.music.set_volume(CONFIGS['VOLUME'])
    Constants().set('game', g)

    running = True
    g.set_screen(MainScreen())
    while running:
        try:
            g.screen.fill('black')
            for ev in g.poll():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if g.get_screen():
                        g.get_screen().key_typed(ev.key, ev.unicode)
                    if g.instance:
                        g.instance.key_typed(ev.key, ev.unicode)
                elif ev.type == pygame.KEYUP:
                    if g.get_screen():
                        g.get_screen().key_released(ev.key, ev.unicode)
                    if g.instance:
                        g.instance.key_released(ev.key, ev.unicode)
                elif ev.type == pygame.MOUSEWHEEL:
                    if g.get_screen():
                        g.get_screen().mouse_scrolled(*pygame.mouse.get_pos(), ev.x, ev.y)
            repeat = g.get_ticker().advance_time(get_system_time())
            for i in range(min(10, repeat)):
                Constants().add('tick', 1)
            g.update()
            g.flip()
            g.fixFrame(360)  # vsync
        except KeyboardInterrupt:
            g.__del__()
        except Exception as e:
            print("Error while handling main:", str(e))
            raise e
    del g
