from src.gui.screen.overlay import Button
from src.gui.screen.screen import Screen
from src.utility.drawutil import DrawUtil


class ResultScreen(Screen):
    def _main(self):
        self.game.finish()
        self.game.main_display()

    def __init__(self, result):
        super().__init__()
        self.overlays.append(Button("home", 5, 5, None, None, False, self._main, size=18))
        self.result = result

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        super().draw_screen(mouse_x, mouse_y, partial_ticks)
        for i, obj in enumerate(self.result.items()):
            name, res = obj
            okays, misses = res
            DrawUtil().draw_box(5 + i * 250, 50, 200, 250, 0xff212121)
            DrawUtil().draw_string(name, 5 + i * 250, 230, 0xffffffff)

            DrawUtil().draw_string('okays', 5 + i * 250, 80, 0xffffffff)
            DrawUtil().draw_string(f'{okays}', 5 + i * 250, 100, 0xffffffff)
            DrawUtil().draw_string('misses', 5 + i * 250, 130, 0xffffffff)
            DrawUtil().draw_string(f'{misses}', 5 + i * 250, 150, 0xffffffff)

