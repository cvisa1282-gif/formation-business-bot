import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from database import init_db
from handlers import start, main_menu, show_profile, buy_credits_menu, handle_text
from admin import handle_payment_callback, handle_withdrawal_callback, top_promoters_admin

print("🚀 Formation Business Bot - Mode Render")

def main():
    init_db()

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(handle_payment_callback))
    application.add_handler(CallbackQueryHandler(handle_withdrawal_callback))
    application.add_handler(CallbackQueryHandler(top_promoters_admin, pattern="^give_500_"))

    print("✅ Tous les handlers chargés")
    print("✅ Police 👮 actif")
    print("✅ Bot prêt pour webhook")

    # Pour Render : on ne lance pas run_polling(), on laisse Render gérer
    # On définit le webhook manuellement plus tard

    port = int(os.environ.get("PORT", 8443))
    print(f"✅ Bot prêt sur port {port} (Webhook mode)")

    # On garde l'application en mémoire
    return application

if __name__ == "__main__":
    print("✅ main.py chargé avec succès OK")
    app = main()
    # Ne rien lancer ici, Render va juste exécuter le fichier
    print("🚀 En attente de configuration webhook...")
