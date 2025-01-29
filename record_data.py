# This file generates random temperature and humidity results instead of the sensors/ In the next level, we will exchange with actual sensors
import os
from datetime import datetime
import random

# Path to the record file
LOG_FILE = "/home/pi/record.txt"

# Function to simulate temperature and humidity readings
def get_temperature_and_humidity():
    temperature = round(random.uniform(20.0, 30.0), 2)  # Random temperature in Celsius
    humidity = round(random.uniform(40.0, 60.0), 2)  # Random humidity percentage
    return temperature, humidity

# Function to record data into the log file
def record_data():
    try:
        # Get the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get simulated sensor readings
        temperature, humidity = get_temperature_and_humidity()
        
        # Write each part of the log entry on a new line
        with open(LOG_FILE, "a") as file:
            file.write(f"Time: {current_time}\n")
            file.write(f"Temperature: {temperature}°C\n")
            file.write(f"Humidity: {humidity}%\n")
            file.write("---\n")  # Separator for readability
        
        print(f"Data recorded:\nTime: {current_time}\nTemperature: {temperature}°C\nHumidity: {humidity}%")
    except Exception as e:
        print(f"Error recording data: {e}")

# Command to execute the script
if __name__ == "__main__":
    print("Executing record_data.py to log temperature and humidity...")
    record_data()
