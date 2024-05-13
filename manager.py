import paho.mqtt.client as mqtt
import random
import sqlMethodes
from icecream import ic


# Callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe(topic)


def on_message(client, userdata, message):
    topic = message.topic
    device = topic.split("/")[-1]
    if 'keepAlive' in topic:
        KAmsg = message.payload.decode("utf-8")
        parseKAmsg = KAmsg.split(":")
        uptime_seconds = parseKAmsg[1].strip()
        sqlMethodes.update_keepAlive(device, uptime_seconds)
        return
    value_or_status = message.payload.decode("utf-8")
    # Extract relevant information from the message
    if value_or_status == 'on':
        status = "on"
        value = sqlMethodes.get_device_value(device)
        print(f"{device} turned on")
    elif value_or_status == 'off':
        status = "off"
        value = sqlMethodes.get_device_value(device)
        print(f"{device} turned off")
    else:
        value = value_or_status
        if "rgb" in value:
            value = value.split("(")[1].split(")")[0]
            print(f"RGB set to: ({value})")
        elif device == 'Airconditioner':
            print(f"AC set to {value}º")
        elif device == 'WaterLevel':
            print(f"The water level is {value}mm")
            sqlMethodes.update_db(device, 'on', value)
            return
        elif device == 'DH-11_Humidity':
            print(f"Humidity in the room is: {value}%")
            sqlMethodes.update_db(device, 'on', value)
            return
        elif device == 'DH-11_Temperature':
            print(f"Temp in the room is: {value}º")
            sqlMethodes.update_db(device, 'on', value)
            if int(value) > 28:
                turn_on_AC()
            return

        status = sqlMethodes.get_device_status(device)

    # Update the database
    sqlMethodes.update_db(device, status, value)


def on_disconnect(userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")


def turn_on_AC():
    sqlMethodes.update_db('Airconditioner', 'on', sqlMethodes.get_device_value('Airconditioner'))
    # client.publish("DvirH/Airconditioner", "on") ToDo check/make it work
    print("A/C turned on")


if __name__ == "__main__":
    # MQTT settings
    broker_address = "broker.hivemq.com"
    topic = "DvirH/#"
    # topic = "DvirH/keepAlive/#"

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
