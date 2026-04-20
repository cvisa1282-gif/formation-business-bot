from fastapi import FastAPI, Request
import uvicorn
import os
from main import main as create_bot

app = FastAPI()
bot_application = create_bot()

@app.get("/")
async def root():
    return {"status": "Bot is running - Formation Business Bot"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/8715926991:AAHI2eIw8uRI0tywk0HJqEdrocJ_RnSW84M")
async def webhook(request: Request):
    try:
        update = await request.json()
        await bot_application.update_queue.put(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error"}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Bot lancé sur port {port} avec webhook")
    uvicorn.run("app:app", host="0.0.0.0", port=port)
