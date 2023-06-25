import threading

import pygame
from mutagen.mp3 import MP3

from .base import BasedInGame
from src.ws.client import Client
from ..screen.overlay import Button
from ...static.constants import Constants
from ...utility.drawutil import DrawUtil
from ...utility.soundutil import SoundUtil
from ...utility.timestamp import get_system_time


class PlayerGame(BasedInGame):
    def _back(self):
        self.ws.shutdown()
        Constants().get('game').finish()
        Constants().get('game').main_display()

    def __init__(self, parent, host: str, nickname: str):
        self.ws = Client(host, nickname)
        self.notes = []
        self.btn = [
            Button("back", 5, 5, None, None, False, self._back)
        ]
        self.okays = 0
        self.misses = 0
        self.parent = parent
        self.song = None
        self.muslen = 100000000
        self.delay = None
        self._played = False
        threading.Thread(target=self.ws.initialize).start()

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        for btn in self.btn:
            btn.draw_screen(mouse_x, mouse_y, partial_ticks)
        if not self.song:
            if not self.ws.running:
                DrawUtil().draw_centered_string("connecting", 1280 / 2, 720 / 2, 0xffffffff)
                if self.ws.reason:
                    Constants().get('game').finish()
                    Constants().get('game').set_screen(self.parent)
                    self.parent.fail_with(self.ws.reason)
            else:
                for i, name in enumerate(self.ws.users):
                    DrawUtil().draw_box(50 + i * 140, 100, 120, 200, 0xff212121)
                    DrawUtil().draw_string(name, 50 + i * 140, 280, 0xffffffff)
        else:
            if not self._played and get_system_time() - self.delay > 0:
                self._played = True
                self.muslen = MP3(f'resources/map/{self.song}/{self.song}.mp3').info.length * 1000
                SoundUtil().play(f'resources/map/{self.song}/{self.song}.mp3')

            if get_system_time() - self.delay > self.muslen:
                self.ws.send({
                    'type': 'finished',
                    'okay': self.okays,
                    'miss': self.misses
                })
            offset = get_system_time() - self.delay
            center_x = 1280 / 2
            note_width = 120
            rem = []
            DrawUtil().draw_box(center_x - note_width * 2, 680, note_width * 4, 20, 0xff424242)
            DrawUtil().draw_box(center_x - 1, 0, 2, 720, 0xffffffff)
            for item in self.notes:
                time, pos = item
                if time + 500 < offset:
                    self.misses += 1
                    rem.append(item)
                pos -= 2
                DrawUtil().draw_box(center_x + note_width * pos, 680 - (time - offset), note_width, 20, 0xffffffff)
            for d in rem:
                self.notes.remove(d)

        DrawUtil().draw_string(f"started: {self.ws.started}, okay|miss: {self.okays}|{self.misses}", 120, 5, 0xffffffff)

    def key_typed(self, key: int, char: str):
        o = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
        offset = get_system_time() - self.delay
        v = {pygame.K_d: False, pygame.K_f: False, pygame.K_j: False, pygame.K_k: False}
        dels = []
        for item in self.notes:
            time, pos = item
            if key == o[pos]:
                if -100 < time - offset < 100 and not v[key]:
                    v[key] = True
                    dels.append(item)
                    self.okays += 1
        for de in dels:
            self.notes.remove(de)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        for btn in self.btn:
            btn.mouse_clicked(mouse_x, mouse_y, mouse_button)
