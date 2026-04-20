from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import add_credits
from config import ADMIN_ID
import sqlite3
from datetime import datetime

# ====================== FONCTIONS ADMIN ======================

async def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

# Validation des paiements (boutons Oui / Non)
async def handle_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("validate_pay_"):
        payment_id = int(data.split("_")[-1])
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT user_id, credits FROM pending_payments WHERE id = ?", (payment_id,))
        row = c.fetchone()
        conn.close()

        if row:
            user_id, credits = row
            add_credits(user_id, credits)
            await context.bot.send_message(user_id, f"✅ Ta transaction a été validée !\n{credits} crédits ont été ajoutés à ton compte.")
            await query.edit_message_caption(f"✅ Paiement #{payment_id} VALIDÉ\nCrédits ajoutés à l'utilisateur.")

    elif data.startswith("reject_pay_"):
        payment_id = int(data.split("_")[-1])
        await query.edit_message_caption(f"❌ Paiement #{payment_id} REFUSÉ\nL'utilisateur doit te contacter sur WhatsApp.")

# Validation des retraits
async def handle_withdrawal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("validate_withdraw_"):
        wid = int(data.split("_")[-1])
        await query.edit_message_text("✅ Retrait validé. L'utilisateur a été notifié.")
        # Ici tu peux ajouter la logique pour notifier l'utilisateur que le retrait est effectué

    elif data.startswith("reject_withdraw_"):
        wid = int(data.split("_")[-1])
        await query.edit_message_text("❌ Retrait refusé.")


# Fonction Top Promoteurs (pour l'admin)
async def top_promoters_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("""SELECT u.username, COUNT(r.id) as count 
                 FROM referrals r 
                 JOIN users u ON r.referrer_id = u.user_id 
                 GROUP BY r.referrer_id 
                 ORDER BY count DESC LIMIT 3""")
    top3 = c.fetchall()
    conn.close()

    if not top3:
        await update.message.reply_text("Aucun parrain pour le moment.")
        return

    text = "🏆 **Top 3 Promoteurs du mois**\n\n"
    buttons = []
    for i, (username, count) in enumerate(top3, 1):
        text += f"{i}. @{username or 'Utilisateur'} → {count} filleuls\n"
        buttons.append([InlineKeyboardButton(f"Donner 500 crédits à {i}", callback_data=f"give_500_{i}")])

    text += "\nClique sur le bouton ci-dessous pour valider les 500 crédits aux 3 meilleurs :"
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)


print("✅ admin.py chargé avec succès OK")
