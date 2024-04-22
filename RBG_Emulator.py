import paho.mqtt.client as mqtt
import time

# MQTT settings
broker_address = "broker.hivemq.com"
topic = "DvirH/Light/RGB"

# Function to simulate turning on the light
def turn_on_light():
    print("RGB on")

# Function to simulate turning off the light
def turn_off_light():
    print("RGB off")

# Callback function for when the client receives a message
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    if payload == "1":
        turn_on_light()
    elif payload == "0":
        turn_off_light()

# Create an MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, 1883, 60)

# Subscribe to the topic
client.subscribe(topic)

# Start the MQTT client loop
client.loop_forever()
