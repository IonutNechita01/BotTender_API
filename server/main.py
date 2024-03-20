from fastapi import FastAPI
from bottender.bot_tender import BotTender 

app = FastAPI()

botTender = BotTender()


@app.get("/")
async def read_root():
    return {}

@app.get("/info")
async def info():
    return botTender.toJson()