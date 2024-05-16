import paho.mqtt.client as mqtt
from sqlclass import IoTDatabase

TOPIC = "manager"
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883

def IsKeepAlive(msg_split):
	if "keepalive" in msg_split[0]:
		db.update_data(int(msg_split[1]),keepAlive=msg_split[2])
		return True
	else:
		return False

def IsRGBSensor(msg_split):
	if "rgb" in msg_split[0]:
		if "on" or "off" in msg_split[2]:
			db.update_data(int(msg_split[1]),status=msg_split[2])
		else:
			db.update_data(int(msg_split[1]),value=msg_split[2])
		return True
	else:
		return False

# Define a callback function to handle incoming messages
def on_message_received(client, userdata, message):
    #print(f"Received message on topic '{message.topic}': {message.payload.decode()}")
    msg = message.payload.decode('utf-8')
    print()
    # the 0 check if its keep alive, 1 - the ID, 2 - the msg
    msg_split = msg.split('/')
    IsKeepAlive(msg_split)
    IsRGBSensor(msg_split)
    
    
    
    
if __name__ == "__main__":
    # Initialize the MQTT client
    mqtt_client = mqtt.Client()

    # Set up callback functions
    mqtt_client.on_message = on_message_received

    # Connect to the MQTT broker
    mqtt_client.connect(BROKER_ADDRESS, port=BROKER_PORT)
    mqtt_client.subscribe(TOPIC)
    
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

