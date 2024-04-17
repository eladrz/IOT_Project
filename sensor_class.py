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
      
    def connect(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def keepAlive(self):
        while True:
            current_time = time.time()
            uptime_seconds = int(current_time - self.start_time)
            self.client.publish(self.alive_topic, str(uptime_seconds))
            time.sleep(self.keep_alive_interval)  # Sleep for the keep-alive interval

    def simulate_temperature_sensor(self, min_temp, max_temp,sleep):
        alive_thread = threading.Thread(target=self.keepAlive)
        alive_thread.start()
        while True:
            temperature = random.uniform(min_temp, max_temp)  # Simulating temperature data
            self.client.publish(self.topic, str(round(temperature, 2)))
            time.sleep(sleep)  # Simulate sensor update interval
        alive_thread.join()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

        
