from bluedot.btcomm import BluetoothServer as BltServer
from signal import pause

from bottender.bot_tender import BotTender

botTender = BotTender()
class BluetoothServer:
    def __init__(self):
        self.server = BltServer(onDataReceived)

def onDataReceived(data):
    print("Received: " + data)