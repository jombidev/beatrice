import json

from websockets.sync.server import serve

from src.utility.aes import *


class Server:
    def __init__(self):
        self.players = {}
        self.running = True
        self.started = False

    def shutdown(self):
        try:
            for ws in self.players.keys():
                ws.close()
            self.server.shutdown()
            self.running = False
        except Exception as e:
            print(str(e))

    def send(self, ws, jn):
        ws.send(encrypt(json.dumps(jn)))

    def broadcast(self, msg):
        for ws in self.players.keys():
            self.send(ws, msg)

    def build(self):
        return {
            'type': 'player_update',
            'players': [*self.players.values()]
        }

    def _handle_ws(self, ws):
        self.players[ws] = None
        try:
            for msg in ws:
                try:
                    msg = decrypt(msg)
                except:
                    print('decryption failure')
                    continue
                m = json.loads(msg)
                if m['type'] == 'ping':
                    self.send(ws, {'type': 'pong'})
                    print('pong:', self.players[ws])
                if m['type'] == 'join':
                    if not self.players[ws]:
                        self.players[ws] = m['name']
                        self.broadcast(self.build())

        except Exception as e:
            print('server got error:', str(e))
        finally:
            del self.players[ws]
            self.broadcast(self.build())

    def initialize(self):
        with serve(self._handle_ws, host='localhost', port=65432) as ws:
            self.server = ws
            print('server handled')
            while self.running:
                self.server.serve_forever()

        print('server death')
