import uvicorn
import socket
import json
from threading import Thread
from bottender.bot_tender_ui import BotTenderUI
from bottender.bot_tender import BotTender
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
    
    config = read_config()
    host = get_local_ip()
    http_port = config.get("http_port", 8000)
    
    config["host"] = host
    write_config(config)
    
    # Start HTTP server in a new thread
    http_thread = Thread(target=start_server, args=(host, http_port))
    http_thread.start()
    
    # Start Bluetooth server in a new thread
    bt_thread = Thread(target=start_bluetooth_server)
    bt_thread.start()

    # Start the tkinter main loop in the main thread
    app = BotTenderUI(bot_tender)
    app.mainloop()
