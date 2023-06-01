import pygame

from src.static.constants import Constants
from src.utility.fontfactory import FontFactory, FontType


class DrawUtil:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def draw_image(self, image_dir: str, x: float, y: float, width: float, height: float):
        img = pygame.image.load(image_dir)
        img = pygame.transform.scale(img, (width, height))
        rect = img.get_rect()
        rect.x = x
        rect.y = y

        Constants().get('game').screen.blit(source=img, dest=rect)

    def draw_box(self, x: float, y: float, width: float, height: float, color: int):
        f3 = color >> 24 & 255
        f = color >> 16 & 255
        f1 = color >> 8 & 255
        f2 = color & 255
        pygame.draw.rect(Constants().get('game').screen, color=(f, f1, f2, f3), rect=pygame.Rect(x, y, width, height))

    def draw_string(self, text: str, x: float, y: float, color: int, font: FontType = FontType.ARIAL, size: int = 16):
        f3 = color >> 24 & 255
        f = color >> 16 & 255
        f1 = color >> 8 & 255
        f2 = color & 255
        fontObj = FontFactory().font(font, size)
        # width, height = fontObj.size(text)
        rendered = fontObj.render(text, True, (f, f1, f2, f3))
        rect = rendered.get_rect()
        rect.x = x
        rect.y = y
        Constants().get('game').screen.blit(rendered, rect)

    def draw_centered_string(self, text: str, x: float, y: float, color: int, font: FontType = FontType.ARIAL,
                             size: int = 16):
        f3 = color >> 24 & 255
        f = color >> 16 & 255
        f1 = color >> 8 & 255
        f2 = color & 255
        rendered = FontFactory().font(font, size).render(text, True, (f, f1, f2, f3))
        rect = rendered.get_rect()
        rect.center = (x, y)
        Constants().get('game').screen.blit(rendered, rect)

    def is_hovered(self, mouse_x: int, mouse_y: int, x: float, y: float, width: float, height: float):
        return x <= mouse_x < x + width and y <= mouse_y < y + height
