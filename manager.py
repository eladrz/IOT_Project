import paho.mqtt.client as mqtt
from sensor_class import SensorClient

TOPIC = "manager"
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883

# Define a callback function to handle incoming messages
def on_message_received(client, userdata, message):
    print(f"Received message on topic '{message.topic}': {message.payload.decode()}")

    # Add your code here to process the incoming message, e.g., update the database
    # You can access the message topic and payload using message.topic and message.payload

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

