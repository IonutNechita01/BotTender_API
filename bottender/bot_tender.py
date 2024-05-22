import json
from typing import List

from models.ingredient_model import IngredientModel
from utils.constants import Response
from time import sleep
from threading import Thread


class BotTender:
    _instance = None

    def __new__(cls, *_, **__):
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
        self.availableIngredients = []
        for ingredient in botTenderConfig["availableIngredients"]:
            self.availableIngredients.append(
                IngredientModel.fromJson(ingredient))
        self.maxAvailableIngredientsCount = botTenderConfig["maxAvailableIngredientsCount"]

    def getStatus(self):
        return {
            "status": self.status
        }

    def getId(self):
        return {
            "id": self.id
        }

    def getName(self):
        return {
            "name": self.name
        }

    def getHost(self):
        return {
            "host": self.host
        }

    def setStatus(self, status):
        self.status = status

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "host": self.host,
            "availableIngredients": [ingredient.toJson() for ingredient in self.availableIngredients],
            "maxAvailableIngredientsCount": self.maxAvailableIngredientsCount
        }
    

    def addIngredient(self, ingredient):
        for i in range(len(self.availableIngredients)):
            if self.availableIngredients[i].position == ingredient.position:
                try:
                    self.availableIngredients[i] = ingredient
                    with open("./bottender/bot_tender_config.json", "w") as f:
                        json.dump(self.toJson(), f)
                        f.close()
                except:
                    return {
                        "status": Response.ERROR
                    }
                return {
                    "status": Response.SUCCESS
                }
            
        self.availableIngredients.append(ingredient)
        try:
            with open("./bottender/bot_tender_config.json", "w") as f:
                json.dump(self.toJson(), f)
                f.close()
            return {
                "status": Response.SUCCESS
            }
        except:
            return {
                "status": Response.ERROR
            }
    
    def removeIngredient(self, ingredient):
        for i in range(len(self.availableIngredients)):
            if self.availableIngredients[i].position == ingredient.position:
                self.availableIngredients.pop(i)
                try:
                    with open("./bottender/bot_tender_config.json", "w") as f:
                        json.dump(self.toJson(), f)
                        f.close()
                    return {
                        "status": Response.SUCCESS
                    }
                except:
                    return {
                        "status": Response.ERROR
                    }
        return {
            "status": Response.ERROR
        }
    
    def prepareCocktail(self, cocktail):
        pumpThreads = []
        for ingredient in cocktail.ingredients:
            for availableIngredient in self.availableIngredients:
                if availableIngredient.position == ingredient["position"]:
                    if availableIngredient.quantity <= ingredient["quantity"]:
                        return {
                            "status": "Not enough " + availableIngredient.name
                        }
                    availableIngredient.quantity -= ingredient["quantity"]
                    pumpThreads.append(Thread(target=self.pourIngredient, args=(availableIngredient,)))
                
        for thread in pumpThreads:
            thread.start()

        for thread in pumpThreads:
            thread.join()
        
        try:
            with open("./bottender/bot_tender_config.json", "w") as f:
                json.dump(self.toJson(), f)
                f.close()
            return {
                "status": Response.SUCCESS
            }
        except:
            return {
                "status": "Error saving changes to bot tender config file"
            }
        
    def pourIngredient(self, ingredient):
        sleep(ingredient.quantity * 0.01)

    def encode(self):
        return json.dumps(self.toJson())
