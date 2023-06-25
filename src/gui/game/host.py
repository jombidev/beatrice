import asyncio
import threading

import pygame
from mutagen.mp3 import MP3

from .base import BasedInGame
from src.ws import Server
import socket

from ..screen.impl.musics import MusicSelectScreen
from ..screen.impl.result import ResultScreen
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
        self.muslen = MP3(f'resources/map/{self.song}/{self.song}.mp3').info.length * 1000
        self.timestamp = get_system_time()
        self.btn.clear()

    def __init__(self):
        self.ws = Server()
        self.btn = [
            Button("back", 5, 5, None, None, False, self._back, size=18),
            Button("start", 30, 320, None, None, False, self._start, size=18)
        ]
        self.tmpnote = []
        self.stop = False

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
        else:
            offset = get_system_time() - self.timestamp
            if offset > self.muslen and not self.stop:
                self.stop = True

            if self.stop:
                if len(self.ws.finished) == len(self.ws.players):
                    res = {}
                    for ws, name in self.ws.players.items():
                        res[name] = [*self.ws.finished[ws]]
                    self.ws.broadcast({
                        'type': 'result',
                        'players': res
                    })
                    Constants().get('game').finish()
                    Constants().get('game').set_screen(ResultScreen(res))
                    self.ws.shutdown()
                DrawUtil().draw_centered_string("Waiting for finish...", 1280 / 2, 720 / 2, 0xffffffff)
            center_x = 1280 / 2
            note_width = 120
            DrawUtil().draw_box(center_x - note_width * 2, 680, note_width * 4, 20, 0xff424242)
            DrawUtil().draw_box(center_x - 1, 0, 2, 720, 0xffffffff)
            dq = []
            for item in self.tmpnote:
                time, pos = item
                if offset - time > 1500:
                    dq.append(item)
                pos -= 2
                DrawUtil().draw_box(center_x + note_width * pos, time - offset + 720, note_width, 20, 0xffffffff)
            for q in dq:
                self.tmpnote.remove(q)

    def key_typed(self, key: int, char: str):
        o = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
        if key in o and not self.stop:
            self.tmpnote.append((get_system_time() - self.timestamp, o.index(key)))
            self.ws.broadcast({
                'type': 'note',
                'time': get_system_time() - self.timestamp,
                'notepos': o.index(key)
            })

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        for btn in self.btn:
            btn.mouse_clicked(mouse_x, mouse_y, mouse_button)
