from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()

def startBluetoothServer():
    def onDataReceived(data):
        dataSplited = data.split('/')
        path = dataSplited[0]
        data = dataSplited[1]

        if path == 'info': 
            server.send(botTender.toJson())

        if path == 'host': 
            server.send(botTender.host)
    
    server = BluetoothServer(onDataReceived)
