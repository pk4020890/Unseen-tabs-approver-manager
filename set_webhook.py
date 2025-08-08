import os, requests, json

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
RENDER_URL = os.environ.get("RENDER_URL")  # e.g. https://your-service.onrender.com

if not (BOT_TOKEN and WEBHOOK_SECRET and RENDER_URL):
    raise RuntimeError("Set BOT_TOKEN, WEBHOOK_SECRET and RENDER_URL env vars before running")

url = f"{RENDER_URL}/webhook/{WEBHOOK_SECRET}"
params = {
    "url": url,
    "allowed_updates": json.dumps(["chat_join_request"])
}
resp = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", data=params, timeout=10)
print(resp.status_code)
print(resp.text)
