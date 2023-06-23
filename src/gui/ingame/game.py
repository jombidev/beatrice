import json
from types import SimpleNamespace

from mutagen.mp3 import MP3

from src.config import CONFIGS
from src.gui.guiactions import Drawable, Clickable, Typeable
from src.static.constants import Constants
from src.utility.drawutil import DrawUtil
from src.utility.soundutil import SoundUtil
from src.utility.timestamp import get_system_time


class GameInstance(Drawable, Clickable, Typeable):
    def __init__(self, song_id: int):
        self.is_paused = False
        self.song_id = song_id
        self.path = f'resources/map/{self.song_id}'
        self.start = get_system_time() + 3000  # after 3s
        j = json.loads('\n'.join(open(f'{self.path}/{self.song_id}.json', mode='r').readlines()), object_hook=lambda d: SimpleNamespace(**d))
        self.bpm = j.bpm
        self.song_offset = j.offset + CONFIGS['OFFSET'] * 10
        self.song_data = MP3(f'{self.path}/{self.song_id}.mp3')
        self.playing = False

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        t = get_system_time() - self.start
        tick = int(t / (60 / (self.bpm * 4) * 1000))

        if not self.playing and t + self.song_offset > 0:
            SoundUtil().play(f'{self.path}/{self.song_id}.mp3')
            self.playing = True
        if t > (self.song_data.info.length + 3) * 1000:
            Constants().get("game").finish()

        DrawUtil().draw_string(f'{t}', 50, 50, 0xffffffff)
        DrawUtil().draw_string(f'{tick // 4}', 50, 80, 0xffffffff)
