import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Import des autres fichiers
from config import CREDIT_PACKS, ADMIN_ID, MIN_WITHDRAWAL, CREDIT_TO_CFA
from database import add_credits, get_user
from police import police_check_referral

# ====================== MENU PRINCIPAL ======================
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("💰 Acheter Crédits"), KeyboardButton("🔗 Mon Lien Parrainage")],
        [KeyboardButton("🏆 Top Promoteurs"), KeyboardButton("📚 Boutique Formations")],
        [KeyboardButton("💸 Retrait"), KeyboardButton("👤 Mon Profil")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🎯 Menu Principal de Formation Business Bot :", reply_markup=reply_markup)


# ====================== START + PARRAINAGE ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or f"User_{user_id}"

    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, join_date) VALUES (?, ?, ?)",
              (user_id, username, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    # Gestion du parrainage
    if context.args:
        try:
            referrer_id = int(context.args[0])
            if referrer_id != user_id:
                if await police_check_referral(referrer_id, user_id, context):
                    conn = sqlite3.connect('bot.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO referrals (referrer_id, referred_id, date) VALUES (?, ?, ?)",
                              (referrer_id, user_id, datetime.now().isoformat()))
                    conn.commit()
                    conn.close()
                    add_credits(referrer_id, 20)
                    add_credits(user_id, 10)
                    await context.bot.send_message(referrer_id, "🎉 Nouveau filleul valide ! +20 crédits")
                    await context.bot.send_message(user_id, "🎁 Bienvenue ! +10 crédits offerts par ton parrain")
        except:
            pass

    await update.message.reply_text("👋 Bienvenue dans **Formation Business Bot** !\nGagne des crédits en parrainant et achète des formations exclusives.")
    await main_menu(update, context)


# ====================== MON PROFIL (avec tout ce que tu as demandé) ======================
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Erreur lors du chargement du profil.")
        return

    credits = user[2]   # colonne credits
    retirable_cfa = credits * CREDIT_TO_CFA

    # Filleuls ce mois
    month_start = datetime.now().replace(day=1).isoformat()
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND date >= ?", (user_id, month_start))
    filleuls_mois = c.fetchone()[0]
    conn.close()

    text = f"👤 **Ton Profil**\n\n"
    text += f"💰 Crédits disponibles : **{credits}**\n"
    text += f"👥 Filleuls ce mois : **{filleuls_mois}**\n"
    text += f"💸 Solde retirable : **{retirable_cfa} CFA**\n\n"

    if retirable_cfa < MIN_WITHDRAWAL:
        text += f"⚠️ Montant minimum de retrait : {MIN_WITHDRAWAL} CFA\nTu n'es pas encore éligible au retrait."
    else:
        text += "✅ Tu peux demander un retrait maintenant !"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ====================== ACHAT CRÉDITS ======================
async def buy_credits_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("200 crédits → 2000 CFA", callback_data="buy_2000")],
        [InlineKeyboardButton("500 crédits → 4000 CFA", callback_data="buy_4000")],
        [InlineKeyboardButton("800 crédits → 6000 CFA", callback_data="buy_6000")],
        [InlineKeyboardButton("1500 crédits → 8000 CFA", callback_data="buy_8000")],
        [InlineKeyboardButton("« Retour", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💰 Choisis ton pack de crédits :", reply_markup=reply_markup)


print("✅ handlers.py chargé avec succès OK")
