from sensor_class import SensorClient
BROKER_ADDRESS = "broker.hivemq.com"
TOPIC = "DvirH/Light/RGB"

KEEP_ALIVE_TOPIC = "DvirH/keepAlive/RGB"
KEEP_ALIVE_SLEEP = 2
# TOPIC = "sensors/RGB"
# BROKER_ADDRESS = "localhost"
ID_SENSOR = "RGB_1"

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC,
                          KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP)

    try:
        # Connect to the MQTT broker
        client.connect()
        # Simulate the sensor
        client.simulate_rgb_sensor()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
