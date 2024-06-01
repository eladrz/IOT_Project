from sensor_class import SensorClient
#from sqlclass import IoTDatabase

#BROKER_ADDRESS = 'publicI_P_Address'

CHECK_HUM_SEND = 3
MIN_HUM = 0
MAX_HUM = 100
KEEP_ALIVE_TOPIC = "keepAlive"
KEEP_ALIVE_SLEEP = 2
TOPIC = "Humidity"
BROKER_ADDRESS = "localhost"
ID_SENSOR = "5"
USERNAME = 'username'
PASSWORD = 'password'

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC, KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)

    # Connect to the MQTT broker
    client.connect()
    #db = IoTDatabase()
    #db.init_db()
    #db.create_IOT_dev(int(ID_SENSOR),"humidity", "", "", "room2", dev_pub_topic = "sensors/humidity", dev_sub_topic ="")
    #db.print_database()
    try:
        # Simulate the sensor
        client.simulate_humidity_sensor(MIN_HUM, MAX_HUM, CHECK_HUM_SEND)
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
