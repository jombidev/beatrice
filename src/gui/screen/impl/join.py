from src.gui.game import PlayerGame
from src.gui.screen.overlay import Button
from src.gui.screen.overlay import Input
from src.gui.screen.screen import Screen
from src.utility.drawutil import DrawUtil


class JoinScreen(Screen):
    def __init__(self, parent):
        super().__init__()
        self.input_ip = None
        self.input_nick = None
        self.parent = parent
        self.reason = None

    def _connect(self):
        try:
            a, b, c, d = map(int, self.input_ip.value.split('.'))
        except:
            return
        if not len(self.input_nick.value):
            return
        self.game.start(PlayerGame(self, self.input_ip.value, self.input_nick.value))

    def __back(self):
        self.game.set_screen(self.parent)

    def fail_with(self, reason):
        self.reason = reason

    def init_screen(self):
        self.overlays.clear()
        self.overlays.append(Button("Back", 10, 10, None, None, False, self.__back, size=18))
        self.input_ip = Input("ip address", 50, 50, size=18)
        self.input_nick = Input("nickname", 50, 120, size=18)
        self.overlays.append(self.input_ip)
        self.overlays.append(self.input_nick)
        self.overlays.append(Button("connect", 50, 180, None, None, False, self._connect, size=18))

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        super().draw_screen(mouse_x, mouse_y, partial_ticks)
        try:
            a, b, c, d = map(int, self.input_ip.value.split('.'))
        except:
            DrawUtil().draw_string("It's not ip-format.", 255, 60, 0xffffffff)
        if not len(self.input_nick.value):
            DrawUtil().draw_string("nickname is empty.", 255, 130, 0xffffffff)
        if self.reason:
            DrawUtil().draw_string(self.reason, 200, 200, 0xffffffff)
