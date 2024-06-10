from sensor_class import SensorClient
#from sqlclass import IoTDatabase

#BROKER_ADDRESS = 'publicI_P_Address'

CHECK_DoorLock_SEND = 3
KEEP_ALIVE_TOPIC = "keepalive"
KEEP_ALIVE_SLEEP = 2
TOPIC = "DoorLock"
BROKER_ADDRESS = "localhost"
ID_SENSOR = "3"

USERNAME = 'username'
PASSWORD = 'password'

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
