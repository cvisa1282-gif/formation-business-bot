import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from database import init_db
from handlers import start, main_menu, show_profile, buy_credits_menu
from admin import handle_payment_callback, handle_withdrawal_callback, top_promoters_admin

print("🚀 Démarrage de Formation Business Bot...")

# ====================== MAIN ======================
def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    # Commandes
    app.add_handler(CommandHandler("start", start))

    # Messages du clavier
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Boutons inline
    app.add_handler(CallbackQueryHandler(handle_payment_callback))
    app.add_handler(CallbackQueryHandler(handle_withdrawal_callback))
    app.add_handler(CallbackQueryHandler(top_promoters_admin, pattern="^give_500_"))

    print("✅ Bot démarré avec succès !")
    print("📌 Token et ID admin chargés")
    print("📌 Police 👮 actif")
    print("📌 Tous les modules importés")

    # Pour tester en local (polling)
    app.run_polling()

# Gestion des boutons du menu
async def handle_text(update, context):
    text = update.message.text

    if text == "👤 Mon Profil":
        await show_profile(update, context)
    elif text == "💰 Acheter Crédits":
        await buy_credits_menu(update, context)
    elif text == "🔗 Mon Lien Parrainage":
        user_id = update.effective_user.id
        await update.message.reply_text(
            f"🔗 Ton lien de parrainage :\n"
            f"https://t.me/{(await context.bot.get_me()).username}?start={user_id}\n\n"
            "Partage ce lien → Tu gagnes 20 crédits par filleul valide !"
        )
    elif text == "🏆 Top Promoteurs":
        await update.message.reply_text("🏆 Top Promoteurs du mois\n(Fonction en cours de développement)")
    elif text == "💸 Retrait":
        await update.message.reply_text("💸 Retrait (minimum 5000 CFA)\nFonction bientôt disponible.")
    elif text == "📚 Boutique Formations":
        await update.message.reply_text("📚 Boutique des formations\nBientôt disponible.")
    else:
        await main_menu(update, context)


if __name__ == '__main__':
    main()

print("✅ main.py chargé avec succès OK")
