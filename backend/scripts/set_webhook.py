import sys
import requests

def set_telegram_webhook(bot_token, webhook_url):
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    payload = {"url": webhook_url}
    
    print(f"Setting webhook for bot to {webhook_url}...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python set_webhook.py <TELEGRAM_BOT_TOKEN> <NGROK_URL>")
        print("Example: python set_webhook.py 12345:ABCDE https://abcd.ngrok.io/api/telegram-webhook")
        sys.exit(1)
        
    set_telegram_webhook(sys.argv[1], sys.argv[2])
