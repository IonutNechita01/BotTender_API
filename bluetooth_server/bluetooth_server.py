import json
import time
import subprocess
import requests
from pywifi import PyWiFi, const, Profile
from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()

STATUS_CONNECTED = 0
STATUS_NETWORK_NOT_FOUND = 1
STATUS_INCORRECT_PASSWORD = 2

def connect_to_wifi(ssid, password):
    try:
        wifi = PyWiFi()
        iface = wifi.interfaces()[1]
        iface.scan()
        time.sleep(8)
        network_found = False
        for network_profile in iface.scan_results():
            if network_profile.ssid == ssid:
                network_found = True
                break
        assert network_found, STATUS_NETWORK_NOT_FOUND
        iface.remove_all_network_profiles()
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        profile = iface.add_network_profile(profile)
        iface.disconnect()   
        iface.connect(profile)
        time.sleep(8)
        assert iface.status() == const.IFACE_CONNECTED, STATUS_INCORRECT_PASSWORD
        cmd = ['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid, 'password', password]
        subprocess.run(cmd, check=True)
        return {'status': STATUS_CONNECTED}
    except Exception as eStatus:
        with open("wifi_log.txt", "w") as f:
            f.write(str(eStatus))
        return {'status': str(eStatus)}

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
            if response['status'] == STATUS_CONNECTED:
                subprocess.run(['sudo', 'systemctl', 'restart', 'myservice'], check=True)
                while True:
                    try:
                        response = requests.get(f"http://{botTender.getHost()}:{8000}/")
                        if response.status_code == 200:
                            break
                        time.sleep(2)
                    except requests.exceptions.RequestException:
                        pass
            server.send(prepareResponse(response))

    server = BluetoothServer(onDataReceived)
