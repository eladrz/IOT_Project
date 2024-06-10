from sensor_class import SensorClient
#from sqlclass import IoTDatabase


KEEP_ALIVE_TOPIC = "keepalive"
KEEP_ALIVE_SLEEP = 2
TOPIC = "RGB"
BROKER_ADDRESS = "localhost"
ID_SENSOR = "1"

USERNAME = 'username'
PASSWORD = 'password'

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC,
                          KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)

    try:
        # Connect to the MQTT broker
        client.connect()
        # Simulate the sensor
        client.simulate_rgb_sensor()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
