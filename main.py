from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ChatJoinRequestHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

# Flask app for uptime ping
app = Flask(__name__)

@app.route('/')
def home():
    return "OK - bot running"

def run():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running ✅ — Auto Approver Active")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working fine! ✅")

# Auto Approve Handler
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.chat_join_request.chat.id
    user_id = update.chat_join_request.from_user.id
    await context.bot.approve_chat_join_request(chat_id, user_id)
    print(f"Approved join request from {user_id} in {chat_id}")

if __name__ == '__main__':
    keep_alive()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(ChatJoinRequestHandler(approve_request))

    application.run_polling()
