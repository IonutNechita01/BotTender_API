import uvicorn
import socket
import json
import threading

from bluetooth_server.bluetooth_server import BluetoothServer

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
    BluetoothServer().start()

if __name__ == "__main__":
    serverThread = threading.Thread(target=start_server)
    serverThread.start()
    bluetoothServerThread = threading.Thread(target=start_bluetooth_server)
    bluetoothServerThread.start()
    serverThread.join()
    bluetoothServerThread.join()
    print("All servers started successfully!")


