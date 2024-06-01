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
    #db = IoTDatabase()
    #db.init_db()
    #db.create_IOT_dev(int(ID_SENSOR),"DoorLock", "", "", "room1", dev_pub_topic = "", dev_sub_topic = "sensors/DoorLock")
    #db.print_database()
    try:
        # Simulate the sensor
        client.simulate_doorLock_sensor()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
