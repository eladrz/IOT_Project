from sensor_class import SensorClient

BROKER_ADDRESS = 'publicI_P_Address'

CHECK_WATER_SEND = 3
MIN_WATER = 0
MAX_WATER = 500
KEEP_ALIVE_TOPIC = "sensors/WaterLevel"
KEEP_ALIVE_SLEEP = 2
# TOPIC = "sensors/WaterLevel"
# BROKER_ADDRESS = "localhost"
ID_SENSOR = "4"
USERNAME = 'dvirheller'
PASSWORD = 'Dvir6375831'

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC, KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)

    # Connect to the MQTT broker
    client.connect()
    db = IoTDatabase()
    db.init_db()
    db.create_IOT_dev(int(ID_SENSOR),"WaterLevel", "", "", "room2", dev_pub_topic = "sensors/WaterLevel", dev_sub_topic ="")
    db.print_database()

    try:
        # Simulate the sensor
        client.simulate_waterLevel_sensor(MIN_WATER, MAX_WATER, CHECK_WATER_SEND)
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
