import paho.mqtt.client as mqtt
import random
import time

# MQTT settings
broker_address = "broker.hivemq.com"
temperature_topic = "DvirH/Temperature/DH-11_Temperature"
humidity_topic = "DvirH/Humidity/DH-11_Humidity"

def publish_sensor_data(client, topic, value):
    # Publish the sensor data to the MQTT topic
    client.publish(topic, str(value))

if __name__ == "__main__":
    # Create an MQTT client
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt.Client(client_id)

    # Connect to the MQTT broker
    client.connect(broker_address, 1883, 60)

    try:
        while True:
            # Simulate temperature reading from the sensor (between 20.0 and 30.0)
            temperature = random.randint(20, 30)
            # temperature = 30
            # Simulate humidity reading from the sensor (between 40 and 60)

            humidity = random.randint(40, 60)

            # Publish temperature and humidity readings
            publish_sensor_data(client, temperature_topic, temperature)
            time.sleep(2)
            publish_sensor_data(client, humidity_topic, humidity)

            time.sleep(10)  # Delay between readings
    finally:
        # Disconnect from the MQTT broker
        client.disconnect()
