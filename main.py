import uvicorn
import socket
import json
import threading
import socket

from bluetooth_server.bluetooth_server import startBluetoothServer

with open("config.json", "r") as f:
    configServer = json.load(f)
    f.close()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return "" 

host = get_local_ip()
configServer["host"] = host

def start_server():
    print("Server started at http://" + host + ":8000")
    uvicorn.run("server.main:app", host=host, port=8000, reload=True)

def start_bluetooth_server():
    print("Bluetooth server started")
    startBluetoothServer()

if __name__ == "__main__":
    start_bluetooth_server()
    start_server()

