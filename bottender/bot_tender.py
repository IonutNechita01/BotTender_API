import json

class BotTender:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        with open("./bottender/bot_tender_config.json", "r") as f:
            botTenderConfig = json.load(f)
            f.close()
        with open("./config.json", "r") as f:
            serverConfig = json.load(f)
            f.close()

        self.status = None
        self.id = botTenderConfig["id"]
        self.name = botTenderConfig["name"]
        self.host = serverConfig["host"]

    def getStatus(self):
        return self.status
    
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name

    def getHost(self):
        return self.host
    
    def setStatus(self, status):
        self.status = status
    
    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "host": self.host
        }