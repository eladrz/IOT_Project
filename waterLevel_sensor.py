from sensor_class import SensorClient

BROKER_ADDRESS = "broker.hivemq.com"
TOPIC = "DvirH/WaterLevel"

CHECK_WATER_SEND = 3
MIN_WATER = 0
MAX_WATER = 500
KEEP_ALIVE_TOPIC = "keepalive"
KEEP_ALIVE_SLEEP = 2
# TOPIC = "sensors/WaterLevel"
# BROKER_ADDRESS = "localhost"
ID_SENSOR = "WaterLevel_1"

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC, KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP)

    # Connect to the MQTT broker
    client.connect()

    try:
        # Simulate the sensor
        client.simulate_waterLevel_sensor(MIN_WATER, MAX_WATER, CHECK_WATER_SEND)
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
