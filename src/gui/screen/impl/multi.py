from src.gui.screen.screen import Screen
from src.gui.screen.util.button import Button


class MultiScreen(Screen):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def some(self):
        pass

    def thing(self):
        print("thing")

    def __back(self):
        self.game.set_screen(self.parent)

    def init_screen(self):
        centerX = 1280 / 2
        centerY = 720 / 2
        leftX = centerX - 30 - 350
        rightX = centerX + 30
        sharedY = centerY - 200
        self._Screen__buttons.clear()
        self._Screen__buttons.append(Button("Back", 10, 10, None, None, False, self.__back, size=18))
        self._Screen__buttons.append(Button("Host", leftX, sharedY, 350, 250, False, self.some))
        self._Screen__buttons.append(Button("Join", rightX, sharedY, 350, 250, False, self.thing))

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        super().draw_screen(mouse_x, mouse_y, partial_ticks)

        # DrawUtil().draw_box(1280 / 2, 0, 1, 720, 0xffffffff)