import os
import requests
import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "please_change_this_secret")
CHANNEL_IDS_RAW = os.environ.get("CHANNEL_IDS", "").strip()
if CHANNEL_IDS_RAW:
    CHANNEL_IDS = [int(x.strip()) for x in CHANNEL_IDS_RAW.split(",") if x.strip()]
else:
    CHANNEL_IDS = []

BASE_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

try:
    r = requests.get(f"{BASE_API}/getMe", timeout=10)
    bot_info = r.json().get("result", {})
    BOT_ID = bot_info.get("id")
    BOT_USERNAME = bot_info.get("username")
    logging.info("Bot running as @%s (id=%s)", BOT_USERNAME, BOT_ID)
except Exception as e:
    BOT_ID = None
    logging.warning("Could not fetch bot info at startup: %s", e)


@app.route("/", methods=["GET"])
def index():
    return "OK - bot running", 200


@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    update = request.get_json(force=True, silent=True)
    logging.info("Update received: %s", update and list(update.keys()))
    if not update:
        return jsonify({"ok": False, "reason": "no json"}), 400

    if "chat_join_request" in update:
        req = update["chat_join_request"]
        chat = req.get("chat", {})
        user = req.get("from", {})
        chat_id = chat.get("id")
        user_id = user.get("id")
        logging.info("Join request for chat=%s from user=%s", chat_id, user_id)

        should_approve = False
        if CHANNEL_IDS:
            if chat_id in CHANNEL_IDS:
                should_approve = True
            else:
                logging.info("Chat %s not in CHANNEL_IDS whitelist", chat_id)
        else:
            if BOT_ID:
                try:
                    resp = requests.get(f"{BASE_API}/getChatMember", params={"chat_id": chat_id, "user_id": BOT_ID}, timeout=10)
                    j = resp.json()
                    status = j.get("result", {}).get("status")
                    logging.info("Bot chat member status in %s = %s", chat_id, status)
                    if status in ("administrator", "creator"):
                        should_approve = True
                except Exception as e:
                    logging.warning("Error checking bot admin status: %s", e)

        if should_approve:
            try:
                resp = requests.post(f"{BASE_API}/approveChatJoinRequest", json={"chat_id": chat_id, "user_id": user_id}, timeout=10)
                logging.info("approveChatJoinRequest result: %s", resp.text)
                return jsonify({"ok": True, "approved": True}), 200
            except Exception as e:
                logging.exception("Failed to approve join request: %s", e)
                return jsonify({"ok": False, "error": str(e)}), 500
        else:
            return jsonify({"ok": True, "approved": False}), 200

    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
