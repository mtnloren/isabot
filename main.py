import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from threading import Thread
from flask import Flask

# ===== חלק 1: הגדרת שרת Keep-Alive =====
app = Flask(__name__)

@app.route('/')
def health_check():
    return "🤖 הבוט פועל ומחכה להודעות!", 200

@app.route('/status')
def status():
    return {
        "status": "active",
        "message": "Bot is running"
    }

def run_flask():
    """מריץ את שרת ה-Flask ב-thread נפרד"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# ===== חלק 2: פונקציות הבוט =====
async def start(update, context):
    """פקודת /start"""
    user_name = update.effective_user.first_name
    welcome_message = f"שלום {user_name}! 👋\nהבוט שלך פועל ומוכן לשירות!"
    await update.message.reply_text(welcome_message)

async def echo(update, context):
    """מחזיר כל הודעה שמקבל"""
    user_message = update.message.text
    response = f"📩 קיבלתי: {user_message}"
    await update.message.reply_text(response)

async def help_command(update, context):
    """פקודת /help"""
    help_text = """
🤖 הפקודות הזמינות:
/start - התחלת שיחה עם הבוט
/help - הצגת הודעת עזרה זו

פשוט שלח לי הודעה ואני אחזיר אותה אליך!
    """
    await update.message.reply_text(help_text)

# ===== חלק 3: הפעלת הבוט =====
def main():
    """הפונקציה הראשית"""
    
    # בדיקה שהטוקן קיים
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ שגיאה: BOT_TOKEN לא נמצא במשתני הסביבה!")
        return
    
    # הפעלת שרת Keep-Alive ב-thread נפרד
    print("🚀 מפעיל שרת Keep-Alive...")
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # בניית הבוט
    print("🤖 בונה את הבוט...")
    application = Application.builder().token(bot_token).build()
    
    # הוספת פקודות ומטפלי הודעות
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # הפעלת הבוט במצב Polling
    print("✅ הבוט מתחיל לפעול...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
