import threading

from src.gui.screen.screen import Screen
from src.ws import Server


class HostScreen(Screen):
    def __init__(self):
        super().__init__()
        self.server = Server()
        threading.Thread(target=self.initialize_ws)

    def initialize_ws(self):
        self.server.initialize()

    def init_screen(self):
        pass