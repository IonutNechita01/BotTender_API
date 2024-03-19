import json
import os
import subprocess
from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()


def connect_to_wifi(ssid, password):
    try:
        config_lines = [
            'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
            'update_config=1',
            'country=US',
            '\n',
            'network={',
            '\tssid="{}"'.format(ssid),
            '\tpsk="{}"'.format(password),
            '}'
        ]
        config = '\n'.join(config_lines)
        
        # Ensure proper permissions
        os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
        
        # Write configuration to wpa_supplicant.conf
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
            wifi.write(config)
        
        # Reconfigure wpa_supplicant
        os.popen("sudo wpa_cli -i wlan0 reconfigure")
        
        # Check if an IP address is assigned
        ip_output = subprocess.check_output(['ip', 'addr', 'show', 'wlan0']).decode()
        if 'inet ' in ip_output:
            return {"status": "connected", "message": "Connected to WiFi"}
        else:
            return {"status": "Error", "message": "Failed to obtain IP address."}
    except IOError as e:
        return {"status": "Error", "message": "IOError: {}".format(str(e))}
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
