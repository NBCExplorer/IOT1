from gpiozero import LED
import time
import random
import paho.mqtt.client as mqtt



red = LED(27)
id = '4c006dfc-d38a-46c5-bf64-5e182d84c8cb'
client_name = id + 'temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    temperature = random.randrange(23,27) #change this so it reads temperature from the sensor
    print('Light level:', temperature)

    if temperature > 24:
        red.on()
    else:
        red.off()
    
    time.sleep(3)