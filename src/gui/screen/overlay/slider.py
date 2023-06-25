from src.gui.guiactions import Clickable, Drawable
from src.utility.drawutil import DrawUtil
from src.utility.fontfactory import FontFactory, FontType


class Slider(Drawable, Clickable):
    __dragging = False
    def __init__(self, text: str, x: float, y: float, width: float, height: float, value_changed_listener, min: float = 0.0, max: float = 1.0, value: float = 0.0, size: int = 18):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.listener = value_changed_listener
        self.min = min
        self.max = max
        self.value = value
        self.size = size

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        hover_color = 0xff646464 if self.__dragging else 0xff535353 if self._is_hovered(mouse_x, mouse_y) else 0xff424242

        if self.__dragging:
            v = max(self.min, min(self.max, (mouse_x - self.x) / self.width))
            if v != self.value:
                self.value = v
                self.listener(self.value)

        thing = (self.value - self.min) / (self.max - self.min)
        DrawUtil().draw_box(self.x, self.y, self.width, self.height, color=0xff212121)
        DrawUtil().draw_box(self.x + (self.width - 15) * thing, self.y, 15, self.height, color=hover_color)
        DrawUtil().draw_centered_string(f'{self.value}' if self.__dragging else self.text, self.x + self.width / 2, self.y + self.height / 2, 0xffffffff, size=self.size)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        if self._is_hovered(mouse_x, mouse_y) and mouse_button == 0:
            self.__dragging = True

    def mouse_released(self, mouse_x: int, mouse_y: int, mouse_button: int):
        self.__dragging = False

    def _is_hovered(self, mouse_x, mouse_y) -> bool:
        width, height = FontFactory().font(FontType.ARIAL, self.size).size(self.text)
        return DrawUtil().is_hovered(mouse_x, mouse_y, self.x, self.y, self.width, self.height)
