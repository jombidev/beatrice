from src.screen.guiable import Clickable, Drawable
from src.utility.drawutil import DrawUtil
from src.utility.fontfactory import FontFactory, FontType


class Button(Drawable, Clickable):
    def __init__(self, text: str, x: float, y: float, action):
        self.text = text
        self.x = x
        self.y = y
        self.action = action

    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        width, height = FontFactory().font(FontType.ARIAL, 24).size(self.text)
        DrawUtil().draw_box(self.x - width, self.y - height, width * 2, height * 2, color=0xff424242 if DrawUtil().is_hovered(mouse_x, mouse_y, self.x - width, self.y - height, width * 2, height * 2) else 0xff212121)
        DrawUtil().draw_centered_string(self.text, self.x, self.y, color=0xffffffff, size=24)

    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        width, height = FontFactory().font(FontType.ARIAL, 24).size(self.text)
        if DrawUtil().is_hovered(mouse_x, mouse_y, self.x - width, self.y - height, width * 2, height * 2):
            self.action()

    def mouse_released(self, mouse_x: int, mouse_y: int, mouse_button: int):
        pass