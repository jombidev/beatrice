import threading
import time

from src.instances import Timer
from src.screen.screen import Screen
from src.utility.drawutil import DrawUtil
from src.utility.soundutil import SoundUtil


class GameScreen(Screen):
    __timestamp = 0.0
    __timing = []
    __is_first = True

    def __delayed_run(self):
        time.sleep(60 / self.bpm * 4)
        SoundUtil().play(self.song)

    def __init__(self, obj, duration: float):
        super().__init__()
        self.bpm = obj["bpm"]
        self.duration = duration
        self.song_path = obj['music']
        self.beat_sound = SoundUtil().build('resources/t.wav')
        self.song = SoundUtil().build(self.song_path)
        self.__timer = Timer(self.bpm / 60)
        self.__timer.last_ms = self._time() + obj['offset']
        self.__timestamp = self._time()

        threading.Thread(target=self.__delayed_run).start()

    def _time(self) -> int:
        return time.time_ns() // 1000000

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        a = self.__timer.advance_time(self._time())
        # for i in range(min(10, a)):
            # SoundUtil().stop(self.beat_sound)
            # SoundUtil().play(self.beat_sound)

        tick = self.__timer.partial_tick
        if self._time() - self.__timestamp > 60 / self.bpm * 1000 * 2:
            print(self._time() - self.__timestamp, 60 / self.bpm * 1000 * 2)
            self.__timestamp += 60 / self.bpm * 1000
            self.__timing.append((-1, -1))
        slow_offset = 0 if tick < 0.1 else 1 if tick < 0.2 else 2 if tick < 0.3 else 3
        fast_offset = 0 if tick > 0.9 else 1 if tick > 0.8 else 2 if tick > 0.7 else 3
        if len(self.__timing) > 10:
            self.__timing.pop(0)

        for i, t in enumerate(self.__timing):
            o, n = t
            if o == -1:
                s = 'MISS (UNPRESS)'
            else:
                m = min(o, n)
                s = 'PERFECT' if m == 0 else 'GREAT' if m == 1 else 'GOOD' if m == 2 else 'MISS'
                if o == n and s == 'PERFECT': s = 'PURE PERFECT'
                else:
                    if o > n: s += ' (FAST)'
                    else: s += ' (SLOW)'

            DrawUtil().draw_centered_string(s, 200, 80 + i * 15, 0xffffff)

        m = min(slow_offset, fast_offset)
        s = 'PERFECT' if m == 0 else 'GREAT' if m == 1 else 'GOOD' if m == 2 else 'MISS'
        if slow_offset == fast_offset and s == 'PERFECT':
            s = 'PURE PERFECT'
        else:
            if fast_offset > slow_offset: s += ' (FAST)'
            else: s += ' (SLOW)'

        DrawUtil().draw_centered_string(f'{s}', 1280 // 2, 80, 0xffffffff)

        DrawUtil().draw_centered_string(f'{a}', 1280 // 2, 50, 0xffffffff)

    def key_typed(self, key: int, char: str):
        tick = self.__timer.partial_tick
        slow = 0 if tick < 0.1 else 1 if tick < 0.2 else 2 if tick < 0.3 else 3
        fast = 0 if tick > 0.9 else 1 if tick > 0.8 else 2 if tick > 0.7 else 3
        self.__timing.append((slow, fast))
        self.__timestamp = self._time()
        DrawUtil().draw_centered_string(f'{min(slow, fast)}', 1280 // 2, 120, 0xffffffff)
        # if slow == 'MISS' and fast == 'MISS':
        #     self.__miss += min(slow, fast)
        # else:
        #     self.__okay += 1


