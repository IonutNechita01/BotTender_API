from bluedot.btcomm import BluetoothServer
from signal import pause

from bottender.bot_tender import BotTender

botTender = BotTender()

def startBluetoothServer():
    def onDataReceived(data):
        if data == "getHost":
            host = botTender.getHost()
            if host == "":
                host = "None"
            server.sendData(host)
    
    server = BluetoothServer(onDataReceived)
