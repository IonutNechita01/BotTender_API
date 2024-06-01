import uvicorn
import socket
import json
import socket
from bottender.bot_tender_ui import BotTenderUI
from bottender.bot_tender import BotTender
from threading import Thread


from bluetooth_server.bluetooth_server import startBluetoothServer

def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file not found.")
        return {}

def write_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return ""

def start_server(host, port):
    print(f"HTTP server started at http://{host}:{port}")
    uvicorn.run("server.main:app", host=host, port=port, reload=True)

def start_bluetooth_server():
    print("Bluetooth server started")
    startBluetoothServer()

if __name__ == "__main__":
    bot_tender = BotTender()
    app = BotTenderUI(bot_tender)
    ui_thread = Thread(target=app.mainloop)
    ui_thread.start()
    config = read_config()
    host = get_local_ip()
    http_port = config.get("http_port", 8000)

    config["host"] = host
    write_config(config)

    start_bluetooth_server()
    start_server(host, http_port)
