import asyncio
import threading

import pygame

from .base import BasedInGame
from src.ws import Server
import socket

from ..screen.impl.musics import MusicSelectScreen
from ..screen.overlay import Button
from ...static.constants import Constants
from ...utility.drawutil import DrawUtil
from ...utility.soundutil import SoundUtil
from ...utility.timestamp import get_system_time


class HostGame(BasedInGame):
    def _get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(("8.8.8.8", 80))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def _back(self):
        self.ws.shutdown()
        Constants().get('game').finish()
        Constants().get('game').main_display()

    def _start(self):
        selection = self.screen.get_selection()
        if not selection:
            return
        if not len(self.ws.players):
            return
        self.ws.started = True
        self.song = selection['id']
        self.ws.broadcast({
            'type': 'game_start',
            'song': selection['id'],
            'delayed': get_system_time() + 5000
        })
        Constants().get('game').clear_screen()
        SoundUtil().stop()
        SoundUtil().play(f'resources/map/{self.song}/{self.song}.mp3')
        self.timestamp = get_system_time()
        self.btn.clear()

    def __init__(self):
        self.ws = Server()
        self.btn = [
            Button("back", 5, 5, None, None, False, self._back, size=18),
            Button("start", 30, 320, None, None, False, self._start, size=18)
        ]
        self.stop = None
        threading.Thread(target=self.ws.initialize).start()
        self.ip = self._get_ip()

    def init(self):
        self.screen = MusicSelectScreen()
        Constants().get('game').set_screen(self.screen)

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        DrawUtil().draw_string(f"Your IP: {self.ip}", 50, 50, 0xffffffff)
        for btn in self.btn:
            btn.draw_screen(mouse_x, mouse_y, partial_ticks)
        if not self.ws.started:
            for i, name in enumerate(self.ws.players.values()):
                DrawUtil().draw_box(50 + i * 140, 100, 120, 200, 0xff212121)
                DrawUtil().draw_string(name if name else 'connecting', 50 + i * 140, 280, 0xffffffff)

    def key_typed(self, key: int, char: str):
        o = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
        if key in o:
            self.ws.broadcast({
                'type': 'note',
                'time': get_system_time() - self.timestamp,
                'notepos': o.index(key)
            })

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        for btn in self.btn:
            btn.mouse_clicked(mouse_x, mouse_y, mouse_button)
