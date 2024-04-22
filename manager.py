import paho.mqtt.client as mqtt
import random
import sqlMethodes


# Callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, message):
    topic = message.topic
    device = topic.split("/")[-1]
    print(device)
    payload = message.payload.decode("utf-8")
    # Extract relevant information from the message
    status = payload
    # Update the database
    sqlMethodes.update_database(device, status)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")


if __name__ == "__main__":
    # MQTT settings
    broker_address = "broker.hivemq.com"
    topic = "DvirH/#"

    # Create an MQTT client
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Connect to the MQTT broker
    client.connect(broker_address, 1883, 60)

    # Start the MQTT client loop
    client.loop_forever()
