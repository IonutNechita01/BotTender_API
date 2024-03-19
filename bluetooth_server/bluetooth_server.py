import json
import wifi
from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()


def connect_to_wifi(ssid, password):
    try:
        wifi.Scheme.find('wlan0', '').delete()

        wifi_scanner = wifi.Cell.all('wlan0')
        wifi_found = False
        for cell in wifi_scanner:
            if cell.ssid == ssid:
                scheme = wifi.Scheme.for_cell('wlan0', ssid, cell, password)
                scheme.save()
                scheme.activate()
                wifi_found = True
                break
        
        if wifi_found:
            return {
                "status": "success",
                "message": "Connected to WiFi: " + ssid
            }
        else:
            return {
                "status": "error",
                "message": "WiFi network not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def prepareResponse(data):
    print(data)
    return json.dumps(data)


def startBluetoothServer():
    def onDataReceived(data):
        dataSplited = data.split('/')
        path = dataSplited[0]
        data = json.loads(dataSplited[1])
        print(path)
        print(data)

        if path == 'info':
            server.send(prepareResponse(botTender.toJson()))

        if path == 'host':
            server.send(prepareResponse(botTender.getHost()))

        if path == 'wifi-credentials':
            response = connect_to_wifi(data['ssid'], data['password'])
            server.send(prepareResponse(response))

    server = BluetoothServer(onDataReceived)
