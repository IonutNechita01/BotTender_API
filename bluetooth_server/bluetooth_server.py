import json
import time
from bluedot.btcomm import BluetoothServer
from pywifi import PyWiFi, const

from bottender.bot_tender import BotTender

botTender = BotTender()

def connect_to_wifi(ssid, password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    
    try:
        iface.disconnect()
        time.sleep(3)
        iface.scan()
        time.sleep(3)
        network_found = False
        for network in iface.scan_results():
            if network.ssid == ssid:
                network_found = True
                wifi_profile = iface.add_network_profile(network)
                wifi_profile.auth = const.AUTH_ALG_OPEN
                wifi_profile.akm.append(const.AKM_TYPE_WPA2PSK)
                wifi_profile.cipher = const.CIPHER_TYPE_CCMP
                wifi_profile.key = password
                iface.connect(wifi_profile)
                timeout = 30
                start_time = time.time()
                while iface.status() != const.IFACE_CONNECTED:
                    if time.time() - start_time > timeout:
                        raise TimeoutError("Connection timed out")
                    time.sleep(1)
                
                break
        
        if network_found:
            return {"status": "connected"}
        else:
            return {"status": "not found"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
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
