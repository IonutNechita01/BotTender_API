import json
import time
from bluedot.btcomm import BluetoothServer
from pywifi import PyWiFi, const

from bottender.bot_tender import BotTender

botTender = BotTender()

def connect_to_wifi(ssid, password):
    wifi = PyWiFi()
    iface_list = wifi.interfaces()

    try:
        for iface in iface_list:
            print(f"Trying interface: {iface.name()}")
            iface.disconnect()
            time.sleep(5)
            print("Scanning for networks...")
            iface.scan()
            time.sleep(5)

            network_found = False
            print("results found: ", iface.scan_results())
            for network in iface.scan_results():
                print(f"Found network: {network.ssid}")
                if network.ssid == ssid:
                    network_found = True
                    print(f"Connecting to network: {ssid}")
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
                    print("Connected successfully!")
                    return {"status": "connected", "interface": iface.name()}
            
            if network_found:
                break
        
        print("Network not found.")
        return {"status": "not found"}

    except Exception as e:
        print(f"Error occurred: {e}")
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
