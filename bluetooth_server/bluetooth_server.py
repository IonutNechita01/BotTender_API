from bluedot.btcomm import BluetoothServer as BltServer
from signal import pause

from bottender.bot_tender import BotTender

botTender = BotTender()
class BluetoothServer:
    def __init__(self):
        self.server = BltServer()

    def data_received(self, data):
        if data == 'info':
            self.server.send(botTender.getHost)

    def client_connected(self):
        print("Client connected")

    def client_disconnected(self):
        print("Client disconnected")

    def start(self):
        self.server.data_received = self.data_received
        self.server.client_connected = self.client_connected
        self.server.client_disconnected = self.client_disconnected
        pause()