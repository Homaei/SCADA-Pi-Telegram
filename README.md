# SCADA-Pi-Telegram
This is a remote monitoring system that integrates a Raspberry Pi, SCADA system, and Telegram bot to enable full-duplex communication for real-time status updates and command execution. The system allows data extraction from PLC-connected SCADA systems in a water treatment plant and transmits it securely to an online database or server.


# SCADA-PiBot: Secure Remote Monitoring with Raspberry Pi & Telegram Bot  

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry%20Pi-red)
![SCADA](https://img.shields.io/badge/SCADA-Supported-blue)

## 📌 Project Overview  
**SCADA-PiBot** is a full-duplex monitoring system that extracts and transmits **SCADA data** from an industrial **water treatment plant** to an **online database** while allowing real-time **two-way communication** via a **Telegram bot**.  

This project utilizes a **Raspberry Pi Zero** as an intermediary to gather data from the **PLC-connected SCADA system** and relay it securely. Since the **TL-6400 router operates with a SIM card and lacks a public IP**, **Cloudflare Tunnel** is employed to ensure secure remote access.

## ✨ Key Features
✅ **SCADA Data Extraction** – Retrieves operational data from PLC devices.  
✅ **Two-Way Telegram Bot Communication** – Sends status updates and accepts user commands.  
✅ **Cloudflare Tunnel Integration** – Secure remote access without a public IP.  
✅ **Scheduled Monitoring with Crontab** – Periodic Raspberry Pi status updates.  
✅ **Data Forwarding to Online Database** – Transfers SCADA logs in real-time.  
✅ **Router & Network Configuration Exploration** – Investigates possible data extraction methods.




SCADA-PiBot/
│── scripts/
│   ├── record_data.py        # Logs temperature & humidity
│   ├── pre_reboot.py         # Saves logs before reboot & notifies Telegram
│   ├── post_reboot.py        # Sends notification after reboot
│   ├── data_collector.py     # Runs every 2 hours (based on crontab)
│   ├── pi_status.py          # Runs every 6 hours (based on crontab)
│── crontab_config.txt        # Crontab settings for automation
│── README.md                 # Project documentation
│── .gitignore                # Ignore unnecessary files (logs, cache, etc.)
│── logs/                     # Directory for log files (ignored in .gitignore)
│── config.py                 # Configuration settings (API keys, paths, etc.)




---

📡 System Architecture

                        ┌───────────────────────────────┐
                        │     Water Treatment Plant     │
                        └───────────────▲───────────────┘
                                        │
                        ┌───────────────▼──────────────┐
                        │  Windows OS + SCADA System   │
                        └───────────────▲──────────────┘
                                        │
                        ┌───────────────▼──────────────┐
                        │           Router (SIM)       │
                        └───────────────▲──────────────┘
                                        │
                        ┌───────────────▼──────────────┐
                        │      Raspberry Pi Zero       │
                        │ ──────────────────────────── │
                        │  📡 Extracts SCADA Data      │
                        │  🔄 Sends Data via MQTT/API  │
                        │  🔗 Cloudflare Tunnel        │
                        └───────────────▲──────────────┘
                                        │
                        ┌───────────────▼──────────────┐
                        │     Telegram Bot (Two-Way)   │
                        │ ──────────────────────────── │
                        │ 📩 User Commands -> Pi       │
                        │ 📊 Pi Status -> Telegram     │
                        └──────────────────────────────┘


---

## ⚙️ Installation & Setup

### **1. Install Required Packages on Raspberry Pi**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip
pip3 install requests telebot flask paho-mqtt
```

2. Clone the Repository
```bash
git clone https://github.com/Homaei/SCADA-Pi-Telegram.git
cd SCADA-Pi-Telegram
```

3. Set Up the Telegram Bot
Create a Telegram bot using BotFather.
Get the API Token and update config.py.
```bash
TELEGRAM_BOT_TOKEN = "your_bot_token"
AUTHORIZED_USERS = ["user_id1", "user_id2"]
```

4. Set Up Cloudflare Tunnel
Install Cloudflare Tunnel on Raspberry Pi:
```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin
```

Authenticate and create a tunnel:
```bash
cloudflared tunnel login
cloudflared tunnel create scada-pibot
```
Configure the tunnel for secure communication.

5. Enable Crontab for Periodic Status Updates
```bash
crontab -e
```

Add the following line:
```bash
*/5 * * * * python3 /path/to/pi_status.py
```

🚀 Usage
Start the Monitoring System
```bash
python3 main.py
```
Interact with the Telegram Bot


+-------------+------------------------------------+
| Command     | Description                        |
+-------------+------------------------------------+
| /status     | Get Raspberry Pi system status     |
| /scada_data | Fetch latest SCADA readings        |
| /help       | Show available commands            |
+-------------+------------------------------------+


🛠 Future Enhancements

🔍 Improve SCADA Data Extraction (Direct Modbus/OPC-UA access).
📡 Optimize Router Configuration (Intercept PLC traffic).
🔐 Enhance Security Measures (VPN-based tunneling).
📊 Implement Data Visualization (Grafana, InfluxDB integration).

📝 License
This project is licensed under the MIT License.

👥 Contributors
Hubert Homaei, Agustno di Bartelo



---

### **How to Use This README:**
- Replace `YourUsername` with your actual GitHub username.
- Update `config.py` paths and credentials before deploying.
- Modify the **contributors** section if needed.

This README follows GitHub markdown best practices and provides an **easy-to-follow installation guide, clear project overview, and next steps** for potential contributors. 🚀 Let me know if you want further modifications! 😊


