from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ChatJoinRequestHandler, ContextTypes
import os

# Get env variables
TOKEN = os.getenv("BOT_TOKEN")
app_url = os.getenv("APP_URL")

# Flask app for uptime ping
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "OK - bot running"

def run():
    flask_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[LOG] /start command from {update.effective_user.id}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Bot is running ✅ — Auto Approver Active"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[LOG] /status command from {update.effective_user.id}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Bot is working fine! ✅"
    )

# Auto Approve Handler
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.chat_join_request.chat.id
    user_id = update.chat_join_request.from_user.id
    await context.bot.approve_chat_join_request(chat_id, user_id)
    print(f"[LOG] Approved join request from {user_id} in {chat_id}")

if __name__ == '__main__':
    keep_alive()

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    # Auto approve
    app.add_handler(ChatJoinRequestHandler(approve_request))

    print("[LOG] Bot started & polling...")
    app.run_polling()
