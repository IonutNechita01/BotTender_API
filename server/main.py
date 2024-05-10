import json
from fastapi import FastAPI
from bottender.bot_tender import BotTender
from models.cocktail_model import CokctailModel
from models.ingredient_model import IngredientModel 

app = FastAPI()

botTender = BotTender()


@app.get("/")
async def read_root():
    return {}

@app.get("/info")
async def info():
    print(botTender.toJson())
    return botTender.toJson()

@app.post("/host")
async def host():
    return botTender.getHost()

@app.post("/addIngredient")
async def add_ingredient(ingredient: IngredientModel):
    print("Adding ingredient")
    print(ingredient.toJson())
    return botTender.addIngredient(ingredient)

@app.post("/removeIngredient")
async def remove_ingredient(ingredient: IngredientModel):
    print("Removing ingredient")
    print(ingredient.toJson())
    return botTender.removeIngredient(ingredient)

@app.post("/prepareCocktail")
async def prepare_cocktail(cocktail: CokctailModel):
    print("Preparing cocktail")
    print(cocktail.toJson())
    return botTender.prepareCocktail(cocktail)
    