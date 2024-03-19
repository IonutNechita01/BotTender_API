import json
import wifi
import subprocess
from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()

def connect_to_wifi1(ssid, password):
    try:
        # Check if a scheme exists before attempting to delete it
        existing_scheme = wifi.Scheme.find('wlan0', '')
        if existing_scheme:
            existing_scheme.delete()

        wifi_scanner = wifi.Cell.all('wlan0')
        wifi_found = False
        for cell in wifi_scanner:
            if cell.ssid != ssid:
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
    
def connect_to_wifi(ssid, password):
    try:
        subprocess.run(["nmcli", "device", "disconnect", "wlan0"])
        
        subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password])
        
        return {
            "status": "success",
            "message": "Connected to WiFi: " + ssid
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
