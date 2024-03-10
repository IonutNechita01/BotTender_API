import uvicorn
import socket
import json

from bluetooth_server.bluetooth_server import BluetoothServer

with open("config.json", "r") as f:
    configServer = json.load(f)

host = socket.gethostbyname(socket.gethostname())
configServer["host"] = host

if __name__ == "__main__":
    uvicorn.run("server.main:app", host=host, port=8000, reload=True)
    #TODO: remove reload=True when is on raspberry pi
    BluetoothServer().start()


