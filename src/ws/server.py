import asyncio
import json

from websockets.server import serve

from src.utility.aes import decrypt


class Server:
    def __init__(self):
        self.players = []
        self.notes = []

    async def receive(self, ws):
        async for message in ws:
            try:
                _messagetemp = decrypt(message)  # i can't trust the python try except
                message = _messagetemp
            except:
                print("got undecryptable message: " + message)
                continue
            dic = json.loads(message)
            # if dic['type'] == 'join': # TODO: use join packet instead
            #     print("join detected: " + dic['name'])
            #     self.players.append(dic['name'])

    async def initialize(self):
        async with serve(self.receive, port=65432):
            await asyncio.Future()
