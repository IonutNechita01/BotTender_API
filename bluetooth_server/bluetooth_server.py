import json
import time
from pywifi import PyWiFi, const, Profile
from bluedot.btcomm import BluetoothServer

from bottender.bot_tender import BotTender

botTender = BotTender()

def connect_to_wifi(ssid, password):
    STATUS_CONNECTED = 0
    STATUS_NETWORK_NOT_FOUND = 1
    STATUS_INCORRECT_PASSWORD = 2
    try:
        wifi = PyWiFi()
        iface = wifi.interfaces()[1]
        iface.scan()
        time.sleep(8)
        network_found = False
        for network_profile in iface.scan_results():
            print(network_profile.ssid)
            if network_profile.ssid == ssid:
                network_found = True
                break
        assert network_found, STATUS_NETWORK_NOT_FOUND
        print(iface.name())
        print("network found")
        print(iface.status())
        print("before remove")
        print(iface.network_profiles())
        iface.remove_all_network_profiles()
        print("after remove")
        print(iface.network_profiles())
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        iface.add_network_profile(profile)
        print("before connect")
        print(iface.status())
        print(iface.network_profiles())
        iface.connect(profile)
        time.sleep(30)
        print("after connect")
        print(iface.status())
        assert iface.status() == const.IFACE_CONNECTED, STATUS_INCORRECT_PASSWORD
        print("success")
        return {'status': STATUS_CONNECTED}
    except Exception as eStatus:
        print(eStatus)
        return {'status': eStatus.args[0]}

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
