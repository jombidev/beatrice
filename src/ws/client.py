import asyncio
import json

import websockets
from websockets.client import connect

from src.utility.aes import encrypt


class Client:
    def __init__(self, host: str):
        self.host = host
        self.send_queue = []
        self.shutdown = False

    def callback(self, msg):
        pass

    async def listen_message(self, ws):
        while True:
            await asyncio.sleep(0)

            try:
                msg = await ws.recv()
                self.callback(msg)
            except websockets.ConnectionClosed:
                print('connection closed.')
                break
            except Exception as err:
                print('got error: ' + str(err))
                break

    async def initialize(self):
        async with connect(f'ws://{self.host}:65432') as ws:
            await ws.send(encrypt(json.dumps({"type": 'join', 'name': 'hi'})))
            asyncio.ensure_future(self.listen_message(ws))
            while True:
                if self.send_queue:
                    await ws.send(self.send_queue.pop(0))
