from sensor_class import SensorClient
#from sqlclass import IoTDatabase


KEEP_ALIVE_TOPIC = "keepalive"
KEEP_ALIVE_SLEEP = 2
TOPIC = "sensors/RGB"
BROKER_ADDRESS = "localhost"
ID_SENSOR = "1"

USERNAME = 'dvirheller'
PASSWORD = 'Dvir6375831'

if __name__ == "__main__":
    # Create an instance of SensorClient
    client = SensorClient(ID_SENSOR, BROKER_ADDRESS, TOPIC,
                          KEEP_ALIVE_TOPIC, KEEP_ALIVE_SLEEP, USERNAME, PASSWORD)
    	
    #rgb_db = IoTDatabase()
    #rgb_db.init_db()
    #rgb_db.create_IOT_dev(int(ID_SENSOR),"RGB", "#000000", " ", "room1", " ", "sensors/RGB")
    #rgb_db.print_database()
    try:
        # Connect to the MQTT broker
        client.connect()
        # Simulate the sensor
        client.simulate_rgb_sensor()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully disconnect
        client.disconnect()
