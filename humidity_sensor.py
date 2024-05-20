from sensor_class import SensorClient

# BROKER_ADDRESS = "broker.hivemq.com"
BROKER_ADDRESS = 'publicI_P_Address'
USERNAME = 'dvirheller'
PASSWORD = 'Dvir6375831'
TOPIC = "DvirH/Humidity/DH-11_Humidity"

CHECK_HUM_SEND = 3
MIN_HUM = 0
MAX_HUM = 100
KEEP_ALIVE_TOPIC = "DvirH/keepAlive/DH-11_Humidity"
KEEP_ALIVE_SLEEP = 2
# TOPIC = "sensors/humidity"
# BROKER_ADDRESS = "localhost"
ID_SENSOR = "humidity_1"

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC, KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)

    # Connect to the MQTT broker
    client.connect()

    try:
        # Simulate the sensor
        client.simulate_humidity_sensor(MIN_HUM, MAX_HUM, CHECK_HUM_SEND)
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
