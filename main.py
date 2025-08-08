from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ChatJoinRequestHandler, ContextTypes
import os

# ------------------ CONFIG ------------------
TOKEN = os.getenv("BOT_TOKEN")  # Bot token from environment variables
PORT = int(os.getenv("PORT", 8080))  # Render assigns PORT automatically
# ---------------------------------------------

# Flask app for uptime monitoring
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ OK - Bot is running"

def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ---------------- TELEGRAM BOT ----------------
# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("🤖 Bot is running ✅ — Auto Approver Active")

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("📡 Bot is working fine! ✅")

# Auto approve join requests
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.chat_join_request.chat.id
    user_id = update.chat_join_request.from_user.id
    await context.bot.approve_chat_join_request(chat_id, user_id)
    print(f"✅ Approved join request from {user_id} in chat {chat_id}")

# ---------------- RUN ----------------
if __name__ == "__main__":
    keep_alive()  # Start Flask in background

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(ChatJoinRequestHandler(approve_request))

    print("🚀 Bot started successfully!")
    app.run_polling()
