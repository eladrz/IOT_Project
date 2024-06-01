import paho.mqtt.client as mqtt
from sqlclass import IoTDatabase

# TOPIC = "manager"
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
USERNAME = 'username'
PASSWORD = 'password'


# functin: update_data(self, sys_id, name, status, keepAlive, value)
def IsKeepAlive(msg_split,topic):
    try:
        if "keepalive" in topic:
            db.update_data(int(msg_split[0]), keepAlive=msg_split[1])
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive: {e}")


def IsRGBSensor(msg_split,topic):
    try:
        if "RGB" in topic:
            if msg_split[1] == "on" or msg_split[1] == "off":
                db.update_data(int(msg_split[0]), status=msg_split[1])
            else:
                db.update_data(int(msg_split[0]), value=msg_split[1])
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in RGB: {e}")


def IsTempSensor(msg_split,topic):
    try:
        if "Temperature" in topic:
            if msg_split[1] == "on" or msg_split[1] == "off":
                db.update_data(int(msg_split[0]), status=msg_split[1])
            else:
                db.update_data(int(msg_split[0]), value=msg_split[1])
                db.update_data(int(msg_split[0]), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsHumiditySensor(msg_split,topic):
    try:
        if "Humidity" in topic:
            if msg_split[1] == "on" or msg_split[1] == "off":
                db.update_data(int(msg_split[0]), status=msg_split[1])
            else:
                db.update_data(int(msg_split[0]), value=msg_split[1])
                db.update_data(int(msg_split[0]), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsDoorLockSensor(msg_split,topic):
    try:
        if "DoorLock" in topic:
            db.update_data(int(msg_split[0]), value=msg_split[1])
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


def IsWaterLevelSensor(msg_split,topic):
    try:
        if 'WaterLevel' in topic:
            if msg_split[1] == "on" or msg_split[1] == "off":
                db.update_data(int(msg_split[0]), status=msg_split[1])
            else:
                db.update_data(int(msg_split[0]), value=msg_split[1])
                db.update_data(int(msg_split[0]), status="on")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in keepAlive thread: {e}")


# Define a callback function to handle incoming messages
def on_message_received(client, userdata, message):
    topic = message.topic
    msg = message.payload.decode('utf-8')
    msg_split = msg.split('/')
    # 0:keepalive or device; 1:ID; 2:msg.
    if len(msg_split) == 2:
        # Check the type of sensor and handle accordingly
        if IsKeepAlive(msg_split,topic):
            return
        elif IsRGBSensor(msg_split,topic):
            return
        elif IsTempSensor(msg_split,topic):
            return
        elif IsDoorLockSensor(msg_split,topic):
            return
        elif IsWaterLevelSensor(msg_split,topic):
            return
        elif IsHumiditySensor(msg_split,topic):
            return
    else:
        print("Wrong message format!")


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
