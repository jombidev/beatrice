class Clickable:
    def mouse_clicked(self, mouse_x: int, mouse_y: int, mouse_button: int):
        """called when mouse clicked"""
        pass

    def mouse_released(self, mouse_x: int, mouse_y: int, mouse_button: int):
        """called when mouse is released"""
        pass

    def mouse_scrolled(self, mouse_x: int, mouse_y: int, scroll_x: int, scroll_y: int):
        """scroll detection"""
        pass
class Typeable:
    def key_typed(self, key: int, char: str):
        """called when keyboard is typed"""
        pass
class Drawable:
    def draw_screen(self, mouse_x: int, mouse_y: int, partial_ticks: float):
        """drawin scren"""
        pass