import json
import socket

from websockets.sync.server import serve

from src.utility.aes import *


class Server:
    def __init__(self):
        self.players = {}
        self.finished = {}
        self.running = True
        self.started = False

    def _get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(("8.8.8.8", 80))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def shutdown(self):
        for ws in [*self.players.keys()]:
            try:
                ws.close()
            except Exception as e:
                print(str(e))
        self.players.clear()
        try:
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
        print('tried connect')
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
                if m['type'] == 'finished':
                    self.finished[ws] = (m['okay'], m['miss'])

        except Exception as e:
            print('server got error:', str(e))
        finally:
            try:
                del self.players[ws]
                self.broadcast(self.build())
            except:
                return

    def initialize(self):
        with serve(self._handle_ws, host=self._get_ip(), port=65432) as ws:
            self.server = ws
            print('server handled')
            while self.running:
                self.server.serve_forever()

        print('server death')
