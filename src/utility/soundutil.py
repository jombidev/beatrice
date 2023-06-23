import pygame.mixer

class SoundUtil:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def build(self, path) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(path)

    def play(self, song, pos: float = 0.0):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0, pos)

    def is_finished(self) -> bool:
        return pygame.mixer.music.get_busy()

    def stop(self, time: int = 0):
        if time != 0:
            pygame.mixer.music.fadeout(time)
        else:
            pygame.mixer.music.stop()
