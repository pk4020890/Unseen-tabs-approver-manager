import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import ChatJoinRequest

TOKEN = os.getenv("BOT_TOKEN")  # Render me env variable me daloge
# BOT_TOKEN me apna Telegram bot ka token dalna

app = ApplicationBuilder().token(TOKEN).build()

# Auto-approve join requests
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.chat_join_request.chat.id
        user_id = update.chat_join_request.from_user.id
        await context.bot.approve_chat_join_request(chat_id, user_id)
        print(f"Approved: {user_id} in {chat_id}")
    except Exception as e:
        print(f"Error: {e}")

# Status command
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online and running!")

# Handlers
app.add_handler(CommandHandler("status", status_command))
app.add_handler(
    telegram.ext.ChatJoinRequestHandler(approve_request)
)

if __name__ == "__main__":
    print("Bot is starting...")
    app.run_polling()
