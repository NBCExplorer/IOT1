from gpiozero import LED
import time
import random
import paho.mqtt.client as mqtt
import json

red = LED(27)
id = '67e6ce98-537b-414e-871f-f0cbc009ee63' #replace with your own unique id
client_telemetry_topic = id + '/telemetry'
client_name = id + '_temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    temperature = random.randrange(23,27) #replace with actual readings from your sensor
    telemetry = json.dumps({'temperature' : temperature})
    print("Sending telemetry ", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(5)