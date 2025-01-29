import requests
from datetime import datetime

# Telegram bot configuration
BOT_TOKEN = "your_bot_token"
CHAT_IDS = ["ID one", "ID two", "ID three"]

def notify_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {"chat_id": chat_id, "text": message}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Notification sent to Chat ID {chat_id}!")
            else:
                print(f"Failed to send notification to Chat ID {chat_id}: {response.text}")
        except Exception as e:
            print(f"Error sending notification to Chat ID {chat_id}: {e}")

if __name__ == "__main__":
    print("Executing post_reboot.py to notify after system reboot...")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notify_telegram(f"Raspberry Pi rebooted successfully at {current_time}.")
