from sensor_class import SensorClient
#from sqlclass import IoTDatabase

CHECK_TEMP_SEND = 3
MIN_TEMP = 15
MAX_TEMP = 35
KEEP_ALIVE_TOPIC = "keepalive"
KEEP_ALIVE_SLEEP = 2
TOPIC = "Temperature"
BROKER_ADDRESS = "192.168.211.54"
ID_SENSOR = "2"
USERNAME = 'username'
PASSWORD = 'password'

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC,
                          KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)

    # Connect to the MQTT broker
    client.connect()
	
    #db = IoTDatabase()
    #db.init_db()
    #db.create_IOT_dev(int(ID_SENSOR),"temperature", "", "", "room1", dev_pub_topic = "sensors/temperature", dev_sub_topic = "")
    #db.print_database()
    
    try:
        # Simulate the sensor
        client.simulate_temperature_sensor(MIN_TEMP, MAX_TEMP, CHECK_TEMP_SEND)
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
