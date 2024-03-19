import json
import subprocess
from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()

def connect_to_wifi(ssid, password):
    try:
        connected_network = subprocess.run(['iwgetid'], capture_output=True, text=True)
        if ssid in connected_network.stdout:
            print("Already connected to", ssid)
            return {"status": "Already connected"}

        subprocess.run(['sudo', 'iw', 'dev', 'wlan0', 'disconnect'])

        print("Connecting to", ssid)
        subprocess.run(['sudo', 'iw', 'dev', 'wlan0', 'connect', ssid])

        subprocess.run(['sleep', '5'])

        password_output = subprocess.run(['sudo', 'wpa_passphrase', ssid, password], input=password.encode(), stdout=subprocess.PIPE, text=True)
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as f:
            f.write('\n' + password_output.stdout)

        subprocess.run(['sudo', 'wpa_supplicant', '-B', '-i', 'wlan0', '-c', '/etc/wpa_supplicant/wpa_supplicant.conf'])

        subprocess.run(['sleep', '5'])

        subprocess.run(['sudo', 'dhclient', '-r'])
        subprocess.run(['sudo', 'dhclient'])
        
        return {"status": "Connected"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

    
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
