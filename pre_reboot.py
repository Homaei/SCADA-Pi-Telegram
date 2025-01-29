import os
import requests
from datetime import datetime

# Telegram bot configuration
BOT_TOKEN = "your_bot_token"
CHAT_IDS = ["ID one", "ID two", "Id three"]

# Path to save logs
LOG_FILE = "/home/pi/pre_reboot_logs.txt"

def save_current_activities():
    try:
        with open(LOG_FILE, "w") as f:
            uptime = os.popen("uptime").read().strip()
            f.write(f"Uptime: {uptime}\n")

            disk_usage = os.popen("df -h").read().strip()
            f.write(f"Disk Usage:\n{disk_usage}\n")

            memory_usage = os.popen("free -h").read().strip()
            f.write(f"Memory Usage:\n{memory_usage}\n")

            processes = os.popen("ps -aux").read().strip()
            f.write(f"Running Processes:\n{processes}\n")

        return True
    except Exception as e:
        print(f"Error saving activities: {e}")
        return False

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
    print("Executing pre_reboot.py to save system logs and notify before reboot...")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if save_current_activities():
        notify_telegram(f"Raspberry Pi is rebooting at {current_time}. Logs saved successfully.")
    else:
        notify_telegram(f"Raspberry Pi is rebooting at {current_time}. Failed to save logs.")
