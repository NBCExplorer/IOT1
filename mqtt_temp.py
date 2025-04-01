import os
import time
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Unique ID for MQTT topics
DEVICE_ID = "nboisvert"
MQTT_BROKER = "test.mosquitto.org"

# Define MQTT topics
TELEMETRY_TOPIC = f"{DEVICE_ID}/telemetry"
COMMAND_TOPIC = f"{DEVICE_ID}/commands"

# GPIO Setup
LED_PIN = 17  # Use GPIO17 for the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Read temperature from DS18B20
def read_temperature():
    base_dir = "/sys/bus/w1/devices/"
    try:
        device_folder = [d for d in os.listdir(base_dir) if d.startswith("28-")][0]
        device_file = f"{base_dir}{device_folder}/w1_slave"
        with open(device_file, "r") as f:
            lines = f.readlines()
        if "YES" in lines[0]:
            temp_str = lines[1].split("t=")[-1]
            temp_c = float(temp_str) / 1000.0
            return round(temp_c, 2)
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

# MQTT Connection Callback
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(COMMAND_TOPIC)

# MQTT Message Callback (Handles Commands from Server)
def on_message(client, userdata, msg):
    try:
        command = json.loads(msg.payload.decode())
        if "led_on" in command:
            GPIO.output(LED_PIN, GPIO.HIGH if command["led_on"] else GPIO.LOW)
            print(f"LED {'ON' if command['led_on'] else 'OFF'}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Setup MQTT Client
mqtt_client = mqtt.Client(DEVICE_ID)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT Broker
mqtt_client.connect(MQTT_BROKER)
mqtt_client.loop_start()

try:
    while True:
        temperature = read_temperature()
        if temperature is not None:
            payload = json.dumps({"temperature": temperature})
            mqtt_client.publish(TELEMETRY_TOPIC, payload)
            print(f"Sent: {payload}")

            # Turn LED on if temperature > 25�C
            GPIO.output(LED_PIN, GPIO.HIGH if temperature > 25 else GPIO.LOW)
        
        time.sleep(3)

except KeyboardInterrupt:
    print("\nShutting down...")
    GPIO.cleanup()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
