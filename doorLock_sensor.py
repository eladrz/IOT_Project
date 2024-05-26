from sensor_class import SensorClient

BROKER_ADDRESS = 'publicI_P_Address'
USERNAME = 'dvirheller'
PASSWORD = 'Dvir6375831'
TOPIC = "DvirH/DoorLock"

CHECK_DoorLock_SEND = 3
KEEP_ALIVE_TOPIC = "DvirH/keepAlive/DoorLock"
KEEP_ALIVE_SLEEP = 2
# TOPIC = "sensors/humidity"
# BROKER_ADDRESS = "localhost"
ID_SENSOR = "doorLock_1"

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC, KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)

    # Connect to the MQTT broker
    client.connect()

    try:
        # Simulate the sensor
        client.simulate_doorLock_sensor()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
