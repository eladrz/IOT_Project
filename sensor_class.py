import time
import random
import paho.mqtt.client as mqtt
import threading

class SensorClient:
    def __init__(self, client_id, broker_address, topic, alive_topic, keep_alive_interval):
        self.client_id = client_id
        self.broker_address = broker_address
        self.topic = topic
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.start_time = time.time()
        self.alive_topic = alive_topic
        self.keep_alive_interval = keep_alive_interval
        self.source = None  # Initialize source variable
      
    def connect(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        if self.source == "rgb":
            rgb_data = msg.payload.decode('utf-8')
            print(msg.topic+ ": received RGB data:", rgb_data)  # Print received RGB data
        else:
            print(msg.topic+": "+str(msg.payload))

    def keepAlive(self):
        while True:
            current_time = time.time()
            uptime_seconds = int(current_time - self.start_time)
            massage = self.source + ": " + str(uptime_seconds) + " seconds alive"
            self.client.publish(self.alive_topic, massage)
            time.sleep(self.keep_alive_interval)  # Sleep for the keep-alive interval

    def simulate_temperature_sensor(self, min_temp, max_temp,sleep):
        self.source = "temp"
        alive_thread = threading.Thread(target=self.keepAlive)
        alive_thread.start()
        while True:
            temperature = random.uniform(min_temp, max_temp)  # Simulating temperature data
            self.client.publish(self.topic, str(round(temperature, 2)))
            time.sleep(sleep)  # Simulate sensor update interval
        alive_thread.join()
        
    def simulate_rgb_sensor(self):
        self.source = "rgb"
        alive_thread = threading.Thread(target=self.keepAlive)
        alive_thread.start()
        alive_thread.join()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

        
