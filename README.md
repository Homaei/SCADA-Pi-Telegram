## 📌 Project Overview  
**SCADA-PiBot** is a full-duplex monitoring and control system that integrates a **SCADA system, Raspberry Pi, and Telegram bot** to **remotely monitor and manage a water treatment plant**.  

The system extracts **real-time operational data** from **PLCs** connected to the SCADA system and securely transmits it to an **online database**. A **Cloudflare Tunnel** is used to bypass the lack of a public IP and enable secure remote communication. Additionally, operators can send commands via a **Telegram bot** to interact with the system.  

The system architecture consists of:  
- **SCADA System & PLCs** – The primary automation and data acquisition layer.  
- **Raspberry Pi** – Acts as an intermediary, collecting SCADA data and handling remote communication.  
- **Router (SIM-based)** – Connects the system to the internet via a **cellular network**, enabling data transfer.  
- **Cloudflare Tunnel** – Provides a secure way to access the Raspberry Pi remotely.  
- **VPS + Grafana** – Stores SCADA logs in a database and visualizes them in real-time.  
- **Telegram Bot** – Allows operators to receive alerts and send remote commands.  

---

## ✨ Key Features  
✅ **SCADA Data Acquisition** – Extracts real-time data from PLCs using **Modbus**.  
✅ **Two-Way Telegram Bot Communication** – Sends automated alerts and allows remote control of the system.  
✅ **Cloudflare Tunnel for Secure Remote Access** – Eliminates the need for a public IP.  
✅ **Grafana Integration** – Visualizes data on a **VPS-hosted dashboard**.  
✅ **Automated Status Updates** – Periodic reports on system health and network status via **crontab**.  
✅ **Secure Communication** – Prevents unauthorized access using **authentication and encryption**.  
✅ **Data Logging & Storage** – Sends SCADA readings to a **remote database** for analysis.  
✅ **Edge Processing with Raspberry Pi** – Reduces latency by processing alerts locally before sending data.  
✅ **Router-Based Connectivity** – Uses a **SIM card for internet access**, making it ideal for remote locations.  
✅ **Scalable & Modular** – Can be extended to support additional IoT sensors or security features.  




```bash
SCADA-PiBot/
│── scripts/
│   ├── record_data.py        # Logs temperature, humidity, and SCADA parameters
│   ├── pre_reboot.py         # Saves logs before reboot & notifies Telegram
│   ├── post_reboot.py        # Sends notification after reboot
│   ├── data_collector.py     # Collects SCADA data every 2 hours (based on crontab)
│   ├── pi_status.py          # Monitors system status & reports every 6 hours
│   ├── telegram_bot.py       # Manages Telegram bot interactions
│   ├── modbus_reader.py      # Extracts PLC data via Modbus protocol
│   ├── cloudflare_tunnel.py  # Handles secure communication via Cloudflare
│── crontab_config.txt        # Crontab settings for periodic automation
│── README.md                 # Project documentation & setup guide
│── .gitignore                # Ignore unnecessary files (logs, cache, env, etc.)
│── config.py                 # Configuration settings (API keys, paths, bot tokens)
│── SCADA-Pi-Telegram.svg     # System architecture diagram (for README display)
│── requirements.txt          # Python dependencies for easy setup
│── LICENSE                   # License details for open-source usage
```

---

## 📡 System Architecture

![SCADA-Pi-Telegram Architecture](https://github.com/Homaei/SCADA-Pi-Telegram/raw/main/SCADA-Pi-Telegram.svg)



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

```bash
+-------------+------------------------------------+
| Command     | Description                        |
+-------------+------------------------------------+
| /status     | Get Raspberry Pi system status     |
| /scada_data | Fetch latest SCADA readings        |
| /help       | Show available commands            |
+-------------+------------------------------------+
```

🛠 Future Enhancements

🔍 Improve SCADA Data Extraction (Direct Modbus/OPC-UA access).

📡 Optimize Router Configuration (Intercept PLC traffic).

🔐 Enhance Security Measures (VPN-based tunneling).

🗃 Saving data to a PostgreSQL database on a VPS.

📊 Implement Data Visualization via Grafana.

📝 License
This project is licensed under the MIT License.

👥 Contributors
- [Hubert Homaei](https://github.com/homaei) and [Aagustin di Bartolo](https://github.com/Jacklamotta).



---

### **How to Use This README:**
- Replace `YourUsername` with your actual GitHub username.
- Update `config.py` paths and credentials before deploying.
- Modify the **contributors** section if needed.




