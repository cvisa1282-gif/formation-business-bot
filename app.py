from fastapi import FastAPI
import uvicorn
import os
from main import main as create_bot

app = FastAPI()
bot_app = create_bot()

@app.get("/")
async def root():
    return {"status": "Bot is running on Render"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Bot lancé sur port {port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port)
