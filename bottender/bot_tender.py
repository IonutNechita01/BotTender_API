import json


with open("./bottender/bot_tender_config.json", "r") as f:
    botTenderConfig = json.load(f)
with open("../config.json", "w") as f:
    serverConfig = json.load(f)

class BotTender():

    def __init__(self, status=None):
        self.status = status
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
