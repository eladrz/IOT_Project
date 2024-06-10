import paho.mqtt.client as mqtt
from sqlclass import IoTDatabase
import json

# TOPIC = "manager"
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
USERNAME = 'username'
PASSWORD = 'password'


# functin: update_data(self, sys_id, name, status, keepAlive, value)
def IsKeepAlive(jsonMsg, topic):
    try:
        if "keepalive" in topic:
            db.update_data(int(jsonMsg['sys_id']), keepAlive=jsonMsg['payload'])
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive: {e}")


def IsRGBSensor(jsonMsg, topic):
    try:
        if "RGB" in topic:
            if jsonMsg['payload'] == "on" or jsonMsg['payload'] == "off":
                db.update_data(int(jsonMsg['sys_id']), status=jsonMsg['payload'])
            else:
                db.update_data(int(jsonMsg['sys_id']), value=jsonMsg['payload'])
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in RGB: {e}")


def IsTempSensor(jsonMsg, topic):
    try:
        if "Temperature" in topic:
            if jsonMsg['payload'] == "on" or jsonMsg['payload'] == "off":
                db.update_data(int(jsonMsg['sys_id']), status=jsonMsg['payload'])
            else:
                db.update_data(int(jsonMsg['sys_id']), value=jsonMsg['payload'])
                db.update_data(int(jsonMsg['sys_id']), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsHumiditySensor(jsonMsg, topic):
    try:
        if "Humidity" in topic:
            if jsonMsg['payload'] == "on" or jsonMsg['payload'] == "off":
                db.update_data(int(jsonMsg['sys_id']), status=jsonMsg['payload'])
            else:
                db.update_data(int(jsonMsg['sys_id']), value=jsonMsg['payload'])
                db.update_data(int(jsonMsg['sys_id']), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsDoorLockSensor(jsonMsg, topic):
    try:
        if "DoorLock" in topic:
            db.update_data(int(jsonMsg['sys_id']), value=jsonMsg['payload'], status=jsonMsg['payload'])
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsWaterLevelSensor(jsonMsg, topic):
    try:
        if 'WaterLevel' in topic:
            if jsonMsg['payload'] == "on" or jsonMsg['payload'] == "off":
                db.update_data(int(jsonMsg['sys_id']), status=jsonMsg['payload'])
            else:
                db.update_data(int(jsonMsg['sys_id']), value=jsonMsg['payload'])
                db.update_data(int(jsonMsg['sys_id']), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsAirconditionerSensor(jsonMsg, topic):
    try:
        if 'Airconditioner' in topic:
            if jsonMsg['payload'] == "on" or jsonMsg['payload'] == "off":
                db.update_data(int(jsonMsg['sys_id']), status=jsonMsg['payload'])
            else:
                db.update_data(int(jsonMsg['sys_id']), value=jsonMsg['payload'])
                db.update_data(int(jsonMsg['sys_id']), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


# Define a callback function to handle incoming messages
def on_message_received(client, userdata, message):
    topic = message.topic
    msg = message.payload.decode('utf-8')
    jsonMsg = json.loads(msg)
    try:
        # Check the type of sensor and handle accordingly
        if IsKeepAlive(jsonMsg, topic):
            return
        elif IsRGBSensor(jsonMsg, topic):
            return
        elif IsTempSensor(jsonMsg, topic):
            return
        elif IsDoorLockSensor(jsonMsg, topic):
            return
        elif IsWaterLevelSensor(jsonMsg, topic):
            return
        elif IsHumiditySensor(jsonMsg, topic):
            return
        elif IsAirconditionerSensor(jsonMsg, topic):
            return
    except KeyError as e:
        print(f"Wrong message format!: {e}")


if __name__ == "__main__":
    # Initialize the MQTT client
    mqtt_client = mqtt.Client()

    # Set username and password
    mqtt_client.username_pw_set(username=USERNAME, password=PASSWORD)

    # Set up callback functions
    mqtt_client.on_message = on_message_received

    # Connect to the MQTT broker
    mqtt_client.connect(BROKER_ADDRESS, port=BROKER_PORT)
    mqtt_client.subscribe("#")

    #connect to the data base
    db = IoTDatabase()
    db.init_db()

    # Start the MQTT client loop to handle incoming messages
    mqtt_client.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Disconnect from the broker when Ctrl+C is pressed
        mqtt_client.disconnect()
