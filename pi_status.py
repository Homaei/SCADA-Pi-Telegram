import os
import socket
import requests
import subprocess
from datetime import datetime

# Telegram bot certificate (token)
BOT_TOKEN = "YOUR TOKEN"
# List of chat IDs to send messages to
CHAT_IDS = ["ID one", "ID two", "ID three"]

# Path to the record file
LOG_FILE = "/home/pi/record.txt"

# -------------------------------------------------------------------
# UTILITY FUNCTIONS WITH EMOJI MAPPERS
# -------------------------------------------------------------------

def get_emoji(value, thresholds, emoji_set):
    """
    Return an emoji based on the provided value compared to thresholds.
    :param value: Numeric value (e.g., disk usage)
    :param thresholds: Dictionary containing 'red' and 'yellow' threshold values
    :param emoji_set: Dictionary containing emojis for 'red', 'yellow', 'green'
    :return: An emoji string corresponding to the usage level
    """
    if value >= thresholds["red"]:
        return emoji_set["red"]
    elif value >= thresholds["yellow"]:
        return emoji_set["yellow"]
    else:
        return emoji_set["green"]

def get_cpu_temp_emoji(temp):
    """
    Return an emoji based on CPU temperature.
    :param temp: CPU temperature in °C
    :return: '❄️' if temp < 50 else '🔥'
    """
    return "❄️" if temp < 50 else "🔥"

def get_uptime_emoji():
    """
    Return an emoji for uptime (used in message formatting).
    :return: '⏰'
    """
    return "⏰" 

# -------------------------------------------------------------------
# FUNCTIONS FOR RASPBERRY PI STATUS
# -------------------------------------------------------------------

def get_actual_ip_address():
    """
    Retrieve the actual IP address of the Raspberry Pi.
    Uses 'hostname -I' to get all IPs and returns the first one.
    :return: IP address string or an error message
    """
    try:
        result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
        ip_addresses = result.stdout.strip().split()
        return ip_addresses[0] if ip_addresses else "🌐 Unable to retrieve IP"
    except Exception:
        return "🌐 Error getting IP"

def get_uptime():
    """
    Retrieve the system uptime from /proc/uptime and format it in h/m/s.
    :return: Formatted uptime string or an error message
    """
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            hours, remainder = divmod(uptime_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    except Exception:
        return "⏳ Error getting uptime"

def get_wifi_ssid():
    """
    Retrieve the currently connected Wi-Fi SSID using 'iwgetid -r'.
    :return: SSID string or an error message
    """
    try:
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True)
        return result.stdout.strip() if result.stdout.strip() else "📡 Not connected to Wi-Fi"
    except Exception:
        return "📡 Error getting Wi-Fi SSID"

def get_wifi_signal_strength():
    """
    Retrieve the Wi-Fi signal strength for wlan0 interface from iwconfig.
    Parse 'Link Quality' to get a percentage value.
    :return: Signal strength in percentage as float or 0.0 if unable to parse
    """
    try:
        result = subprocess.run(["iwconfig", "wlan0"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Link Quality" in line or "Signal level" in line:
                parts = line.split()
                quality = next((part.split('=')[1] for part in parts if "Quality=" in part), None)
                if quality:
                    numerator, denominator = map(int, quality.split('/'))
                    percentage = (numerator / denominator) * 100
                    return percentage  # Return as float for proper formatting
        return 0.0
    except Exception:
        return 0.0

def get_disk_usage():
    """
    Retrieve disk usage percentage for root filesystem '/' using df -h.
    :return: Disk usage percentage as int or 0 if error occurs
    """
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        usage = int(result.stdout.strip().split("\n")[1].split()[4].replace("%", ""))
        return usage
    except Exception:
        return 0

def get_memory_usage():
    """
    Retrieve memory usage from /proc/meminfo.
    Calculate total memory and available memory to find usage percentage.
    :return: Memory usage percentage as float or 0.0 if error occurs
    """
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
            mem_total = int(lines[0].split()[1]) / 1024
            mem_available = int(lines[2].split()[1]) / 1024
            mem_used = mem_total - mem_available
            usage = (mem_used / mem_total) * 100
            return usage  # Return as float for proper formatting
    except Exception:
        return 0.0

def get_cpu_temperature():
    """
    Retrieve CPU temperature from /sys/class/thermal/thermal_zone0/temp.
    :return: CPU temperature in °C as float or 0.0 if error occurs
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000
            return temp  # Return as float
    except Exception:
        return 0.0

def get_cpu_usage():
    """
    Retrieve CPU usage percentage using 'top -bn1'.
    Parse the line containing 'Cpu(s)' to get the user space usage (us).
    Also determine the emoji based on usage thresholds.
    :return: (usage_value, usage_emoji) as a tuple
    """
    try:
        result = subprocess.run(["top", "-bn1"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Cpu(s)" in line:
                # Extract CPU usage percentage (us - user space usage)
                usage = float(line.split(":")[1].strip().split(",")[0].replace("us", "").strip())
                
                # Assign emoji based on usage thresholds
                if usage < 30:
                    emoji = "🟢"  # Green for low usage
                elif 30 <= usage < 70:
                    emoji = "🟡"  # Yellow for moderate usage
                else:
                    emoji = "🔴"  # Red for high usage
                
                return usage, emoji  # Return both the numeric value and the emoji
        return 0.0, "❓ Unable to determine CPU usage"
    except Exception:
        return 0.0, "❓ Error getting CPU usage"

def get_active_processes():
    """
    Count the number of active processes by running 'ps -e' and subtracting the header line.
    :return: Number of processes as int or error message string
    """
    try:
        result = subprocess.run(["ps", "-e"], capture_output=True, text=True)
        process_count = len(result.stdout.strip().splitlines()) - 1  # Subtract header line
        return process_count
    except Exception:
        return "❓ Error getting active processes"

def get_network_traffic():
    """
    Retrieve network traffic for wlan0 from /proc/net/dev.
    :return: Formatted string showing received and sent data in MB or error message
    """
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines():
                if "wlan0" in line:
                    data = line.split()
                    received = int(data[1]) / (1024 * 1024)
                    sent = int(data[9]) / (1024 * 1024)
                    return f"⬇️ {received:.2f} MB, ⬆️ {sent:.2f} MB"
        return "❓ No data for wlan0"
    except Exception:
        return "❓ Error getting network traffic"

def get_system_load():
    """
    Retrieve system load averages from /proc/loadavg for 1, 5, and 15 minutes.
    :return: String representing the load averages or an error message
    """
    try:
        with open("/proc/loadavg", "r") as f:
            load_avg = f.read().strip().split()[:3]
        return f"1m: {load_avg[0]}, 5m: {load_avg[1]}, 15m: {load_avg[2]}"
    except Exception:
        return "❓ Error getting system load"

def get_usb_devices():
    """
    Retrieve USB devices information using 'lsusb'.
    :return: String listing all USB devices or an error message
    """
    try:
        result = subprocess.run(["lsusb"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "❓ Error getting USB devices"

def read_log_file():
    """
    Read the last 5 lines from the log file defined in LOG_FILE.
    :return: Formatted string containing up to last 5 lines or an error message
    """
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        return "\n".join(lines[-5:]) if lines else "No log data found"
    except FileNotFoundError:
        return "❌ Log file not found"
    except Exception:
        return "❓ Error reading log file"

def get_login_logs():
    """
    Retrieve the last 5 login logs using 'last -n 5'.
    :return: String with login logs or an error message
    """
    try:
        result = subprocess.run(["last", "-n", "5"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "❓ Error getting login logs"

# -------------------------------------------------------------------
# SEND MESSAGE TO TELEGRAM BOT
# -------------------------------------------------------------------

def send_telegram_message(message):
    """
    Send a message to configured Telegram chat IDs using the Telegram Bot API.
    :param message: The message text to send
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        try:
            response = requests.post(url, data={"chat_id": chat_id, "text": message})
            if response.status_code != 200:
                print(f"Failed to send message: {response.text}")
        except Exception as e:
            print(f"Error sending message: {e}")

# -------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------

def main():
    """
    Main function to gather system status information and send it to Telegram.
    """
    try:
        # Collect various system metrics
        ip_address = get_actual_ip_address()
        uptime = get_uptime()
        wifi_ssid = get_wifi_ssid()
        wifi_signal_strength = get_wifi_signal_strength()
        disk_usage = get_disk_usage()
        memory_usage = get_memory_usage()
        cpu_temperature = get_cpu_temperature()
        cpu_usage_value, cpu_usage_emoji = get_cpu_usage()
        active_processes = get_active_processes()
        network_traffic = get_network_traffic()
        system_load = get_system_load()
        usb_devices = get_usb_devices()
        log_data = read_log_file()
        login_logs = get_login_logs()

        # Define thresholds and corresponding emoji sets
        thresholds = {
            "disk": {"red": 66, "yellow": 33},
            "memory": {"red": 80, "yellow": 60},
        }
        emoji_sets = {
            "disk": {"red": "🔴", "yellow": "🟡", "green": "🟢"},
            "memory": {"red": "🔴", "yellow": "🟡", "green": "🟢"},
        }

        # Assign emojis based on thresholds for disk and memory usage
        disk_emoji = get_emoji(disk_usage, thresholds["disk"], emoji_sets["disk"])
        memory_emoji = get_emoji(memory_usage, thresholds["memory"], emoji_sets["memory"])

        # Build the message
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""
📊 Raspberry Pi 1 Status:

🕒 Time: {current_time}
🌐 IP Address: {ip_address}
📡 Wi-Fi SSID: {wifi_ssid}
📶 Wi-Fi Signal Strength: {wifi_signal_strength:.2f}%
⏳ Uptime: {uptime} {get_uptime_emoji()}
🔥 CPU Temperature: {cpu_temperature:.2f}°C {get_cpu_temp_emoji(cpu_temperature)}
💾 Disk Usage: {disk_usage}% {disk_emoji}
📈 Memory Usage: {memory_usage:.2f}% {memory_emoji}
⚙️ CPU Usage: {cpu_usage_value:.2f}% {cpu_usage_emoji}
🖥️ Active Processes: {active_processes}
🌐 Network Traffic: {network_traffic}
📊 System Load: {system_load}
🖴 USB Devices:\n{usb_devices}

📜 Last 5 Log Entries:
{log_data}

🔐 Last 5 Login Logs:
{login_logs}
"""
        # Send the assembled message via Telegram
        send_telegram_message(message)

    except Exception as e:
        print(f"Error in main function: {e}")

# Entry point for script execution
if __name__ == "__main__":
    main()
