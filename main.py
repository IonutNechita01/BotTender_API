import uvicorn
import socket
import json
import threading

from bluetooth_server.bluetooth_server import startBluetoothServer

with open("config.json", "r") as f:
    configServer = json.load(f)
    f.close()

host = socket.gethostbyname(socket.gethostname())
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

