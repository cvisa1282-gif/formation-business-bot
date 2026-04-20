import sqlite3
from datetime import datetime, timedelta
from telegram.ext import ContextTypes

# ====================== POLICE 👮 ULTRA BOOSTÉ ======================
async def police_check_referral(referrer_id: int, new_user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if referrer_id == new_user_id:
        await context.bot.send_message(ADMIN_ID, f"🚨 Police 👮 Self-referral détecté → Utilisateur {new_user_id}")
        return False

    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    # Détection invitations trop rapides (max 8 en 10 minutes)
    ten_min_ago = (datetime.now() - timedelta(minutes=10)).isoformat()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND date > ?", (referrer_id, ten_min_ago))
    count = c.fetchone()[0]

    if count >= 8:
        await context.bot.send_message(
            ADMIN_ID, 
            f"🚨 Police 👮 ALERTE !\n"
            f"Utilisateur {referrer_id} a invité {count} personnes en moins de 10 minutes !\n"
            f"Comportement suspect détecté."
        )
        conn.close()
        return False

    # Tu peux ajouter d'autres règles ici plus tard (multi-comptes, etc.)
    conn.close()
    return True


async def police_log(message: str):
    """Fonction pour logger les alertes Police vers l'admin"""
    await asyncio.sleep(1)  # petit délai pour éviter flood
    # On enverra le message à l'admin dans les handlers qui l'appellent


print("✅ police.py chargé avec succès OK")
