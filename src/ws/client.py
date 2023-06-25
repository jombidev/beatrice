import json
import os
import threading
import time

import websockets
from websockets.sync.client import connect

from src.gui.screen.impl.result import ResultScreen
from src.static.constants import Constants
from src.utility.aes import *


class Client:
    def __init__(self, host: str, name: str):
        self.host = host
        self.name = name
        self.send_queue = []
        self.users = []
        self.client = None
        self.running = False
        self.reason = None
        self.started = False

    def callback(self, msg):
        if msg['type'] == 'pong':
            return
        if msg['type'] == 'player_update':
            self.users.clear()
            for user in msg['players']:
                self.users.append(user)
        if msg['type'] == 'game_start':
            self.started = True
            Constants().get('game').instance.song = msg['song']
            Constants().get('game').instance.delay = msg['delayed']
            Constants().get('game').instance.btn.clear()
        if msg['type'] == 'note':
            Constants().get('game').instance.notes.append((msg['time'], msg['notepos']))

        if msg['type'] == 'result':
            self.shutdown()
            Constants().get('game').finish()
            Constants().get('game').set_screen(ResultScreen(msg['players']))



    def shutdown(self):
        self.running = False

    def listen_message(self):
        while self.running:
            try:
                msg = self.client.recv()
                self.callback(json.loads(decrypt(msg)))
            except websockets.ConnectionClosed:
                print('connection closed - message awaiter')
                self.running = False
                self.reason = 'disconnected'
            except TimeoutError:
                print('message timed out')
                continue
            except Exception as err:
                print('got error: ' + str(err))
                print(err)
                break


    def _send_ping(self):
        print('workin')
        while self.running:
            try:
                time.sleep(15)
                self.send_queue.append({'type': 'ping'})
            except websockets.ConnectionClosed:
                print('connection closed - ping checker')
                self.running = False
                self.reason = 'disconnected'
            except Exception as err:
                print('got error: ' + str(err))
                print(err)
                break

    def send(self, jn):
        try:
            self.client.send(encrypt(json.dumps(jn)))
        except:
            return

    def initialize(self):
        try:
            with connect(f'ws://{self.host}:65432') as ws:
                self.client = ws
                self.running = True
                threading.Thread(target=self._send_ping).start()
                threading.Thread(target=self.listen_message).start()
                print('connected')

                self.send({'type': 'join', 'name': self.name})

                while self.running:
                    if self.send_queue:
                        self.send(self.send_queue.pop(0))

            print('run fin')
        except KeyboardInterrupt:
            self.running = False
            os._exit(0)
        except Exception as e:
            print('got exception:', str(e), type(e))
            if not self.running:
                self.reason = 'invalid_host_or_timed_out'
            else:
                self.reason = 'disconnected'
            self.running = False
        finally:
            if self.client:
                self.client.close()
