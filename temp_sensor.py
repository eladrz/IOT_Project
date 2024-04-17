from sensor_class import SensorClient

CHECK_TIME_SEND_IN_SEC = 3
MIN_TEMP = 15
MAX_TEMP = 35
KEEP_ALIVE_TOPIC = "keepalive"
KEEP_AKIVE_SLEEP = 2
TOPIC = "sensors/temperature"
BROKER_ADDRESS = "localhost"
ID_SENSOR = "temperature_1"

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR ,BROKER_ADDRESS ,TOPIC ,KEEP_ALIVE_TOPIC ,KEEP_AKIVE_SLEEP)

    # Connect to the MQTT broker
    client.connect()

    try:
        # Simulate the sensor
        client.simulate_temperature_sensor(MIN_TEMP,MAX_TEMP,CHECK_TIME_SEND_IN_SEC)
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()

