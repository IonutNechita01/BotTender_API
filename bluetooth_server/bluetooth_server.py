from bluedot.btcomm import BlueetoothServer
from signal import pause

class BluetoothServer:
    def __init__(self):
        self.server = BluetoothServer()

    def data_received(self, data):
        print(data)

    def client_connected(self):
        print("Client connected")

    def client_disconnected(self):
        print("Client disconnected")

    def start(self):
        self.server.data_received = self.data_received
        self.server.client_connected = self.client_connected
        self.server.client_disconnected = self.client_disconnected
        pause()