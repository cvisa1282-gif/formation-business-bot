from main import main
import os
from telegram.ext import Application

app = main()

# Render fournit la variable PORT
PORT = int(os.environ.get("PORT", 8443))

print(f"✅ Webhook prêt sur port {PORT}")

# Pour le moment on garde simple - on configurera le webhook complet plus tard si besoin
if __name__ == "__main__":
    print("🚀 Bot en attente de webhook...")
