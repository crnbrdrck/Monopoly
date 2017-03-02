from json import dumps
from socket import *


class TestClient(socket):

    def send_create(self, username='Guest', password=None):
        msg = dumps({'command': 'CREATE', 'values': {'game': 'Monopoly', 'username': username, 'password': password}})
        self.sendall(msg.encode())

    def send_join(self, username='', password=None):
        msg = dumps({'command': 'JOIN', 'values': {'game': 'Monopoly', 'username': username, 'password': password}})
        self.sendall(msg.encode())

    def send_start(self):
        msg = dumps({'command': 'START', 'values': {}})
        self.sendall(msg.encode())