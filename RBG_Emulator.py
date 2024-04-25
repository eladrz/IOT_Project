import paho.mqtt.client as mqtt
import time

# MQTT settings
import sqlMethodes

broker_address = "broker.hivemq.com"
topic_rgb = "DvirH/Light/RGB"
topic_color = "DvirH/Light/Color"


# Function to simulate turning on the light
def turn_on_light():
    print("RGB on")


# Function to simulate turning off the light
def turn_off_light():
    print("RGB off")


# Function to handle color change
def change_light_color(rgb_value):
    print(f"RGB color set to: {rgb_value}")


# Callback function for when the client receives a message
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    if message.topic == topic_rgb:
        if payload == "on":
            turn_on_light()
            sqlMethodes.update_db('RGB', 'on', sqlMethodes.get_device_value("RGB"))
        elif payload == "off":
            turn_off_light()
            sqlMethodes.update_db('RGB', 'off', sqlMethodes.get_device_value("RGB"))
    elif message.topic == topic_color:
        change_light_color(payload)
        rgb_values = payload.split("(")[1].split(")")[0]
        sqlMethodes.update_db('RGB', sqlMethodes.get_device_status("RGB"), rgb_values)


# Create an MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, 1883, 60)

# Subscribe to the topics
client.subscribe(topic_rgb)
client.subscribe(topic_color)

# Start the MQTT client loop
client.loop_forever()
