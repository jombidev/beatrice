import json
import os
import time
from types import SimpleNamespace

from src.screen.screen import Screen
from src.utility.drawutil import DrawUtil
from src.utility.fontfactory import FontType
from src.utility.soundutil import SoundUtil


class MusicSelectScreen(Screen):
    __finalScroll = 0.0
    __scrollAnimation = 0.0
    __musicList = []
    __selected = None
    __playing = None
    __recheck = 0.0

    def __load_music_list(self):
        self.__musicList.clear()
        validPack = ['jpg', 'json', 'mp3']
        for f in os.listdir('resources/map'):
            dir = 'resources/map/' + f
            valid = True
            for ext in validPack:
                if not os.path.exists(f'{dir}/{f}.{ext}'):
                    valid = False
            if not valid:
                continue
            j = json.loads('\n'.join(open(f'{dir}/{f}.json', mode='r').readlines()), object_hook=lambda d: SimpleNamespace(**d))
            self.__musicList.append({
                'name': f'{j.name} - {j.composer}',
                'bpm': j.bpm,
                'highlight': j.highlight,
                'duration': j.highlightDuration,
                'image': f'{dir}/{f}.jpg',
                'music': f'{dir}/{f}.mp3',
                'beatmap': j
            })

    def init_screen(self):
        self.__load_music_list()

    def __max_scroll(self) -> float:
        return max(0.0, len(self.__musicList) * 100 - 720 + 50)

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        self.__finalScroll += self.__scrollAnimation / 10

        self.__scrollAnimation -= self.__scrollAnimation / 10
        if -0.01 < self.__scrollAnimation < 0.01 and self.__scrollAnimation != 0.0:
            self.__scrollAnimation = 0.0
        if self.__playing:
            thing = self.__selected['duration'] - (self.__playing and time.time_ns() // 1000000 - self.__recheck)
            print(thing)
            if thing < 1500:
                print(thing / 1500)
                self.__playing.setVolume_(thing / 1500)

        if self.__playing and time.time_ns() // 1000000 - self.__recheck > self.__selected['duration']:
            SoundUtil().stop(self.__playing)
            SoundUtil().play(self.__playing, self.__selected['highlight'])
            self.__recheck = time.time_ns() // 1000000

        self.__draw_list(80, 30, -self.__finalScroll, mouse_x, mouse_y)
        self.__draw_selected(720, 50)
        self.__finalScroll = max(0.0, min(self.__max_scroll(), self.__finalScroll))

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        x = 80
        y = 30 - self.__finalScroll
        width = 600
        height = 100
        for i in range(len(self.__musicList)):
            if DrawUtil().is_hovered(mouse_x, mouse_y, x, y + i * height, width, height):
                self.__selected = None if self.__selected is not None and self.__selected == self.__musicList[i] else self.__musicList[i]
                if self.__playing:
                    SoundUtil().stop(self.__playing)
                    self.__playing = None
                if self.__selected:
                    thing = SoundUtil().build(self.__selected['music'])
                    self.__playing = thing
                    self.__recheck = time.time_ns() // 1000000
                    SoundUtil().play(self.__playing, self.__selected['highlight'])

    def mouse_scrolled(self, mouse_x: int, mouse_y: int, scroll_x: int, scroll_y: int):
        self.__scrollAnimation -= scroll_y * 10

    def __draw_list(self, x: float, y: float, scroll: float, mouse_x: int, mouse_y: int):
        original_y = y
        y += scroll
        width = 600
        height = 100
        DrawUtil().draw_box(x, y, width, height * len(self.__musicList), 0xff212121)
        for i in range(len(self.__musicList)):
            if DrawUtil().is_hovered(mouse_x, mouse_y, x, y + i * height, width, height) or self.__selected == self.__musicList[i]:
                DrawUtil().draw_box(x, y + i * height, width, height, 0xff424242)
            DrawUtil().draw_box(x, y + i * height, width, 1, 0xff424242)
            DrawUtil().draw_image(self.__musicList[i]['image'], x, y + i * height, height, height)
            DrawUtil().draw_string(self.__musicList[i]['name'], x + height + 5, y + i * height + 5, 0xffffffff, font=FontType.NANUM, size=20)
            DrawUtil().draw_string(f'BPM: {self.__musicList[i]["bpm"]}', x + height + 5, y + i * height + 5 + 20, 0xffffffff, font=FontType.NANUM)

    def __draw_selected(self, x: int, y: int):
        width = 450
        height = 600
        if self.__selected:
            DrawUtil().draw_box(x, y, width, height, 0xff212121)
            DrawUtil().draw_image(self.__selected['image'], x + width / 2 - 100, y + 25, 200, 200)
            DrawUtil().draw_centered_string(self.__selected['name'], x + width / 2, y + 250, 0xffffffff, font=FontType.NANUM, size=24)
            DrawUtil().draw_centered_string(f'BPM: {self.__selected["bpm"]}', x + width / 2, y + 265 + 15, 0xffffffff, font=FontType.NANUM)
