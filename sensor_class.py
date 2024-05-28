import time
import random
import paho.mqtt.client as mqtt
import threading
import tkinter as tk
from guiSensors import *

TOPIC_MANAGER = "manager"

class SensorClient:
    def __init__(self, client_id, broker_address, topic, alive_topic, keep_alive_interval, username=None, password=None):
        self.client_id = client_id
        self.broker_address = broker_address
        self.username = username
        self.password = password
        self.topic = topic
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.start_time = time.time()
        self.alive_topic = alive_topic
        self.keep_alive_interval = keep_alive_interval
        self.source = None  # Initialize source variable

    def connect(self):
        try:
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.broker_address)
            self.client.loop_start()
        except Exception as e:
            print(f"Error connecting to broker: {e}")

    def on_connect(self, client, userdata, flags, rc):
        try:
            print("Connected with result code " + str(rc))
            self.client.subscribe(self.topic)
        except Exception as e:
            print(f"Error subscribing to topic: {e}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        print(payload)
        manager_msg =  self.source + "/" + self.client_id + "/" + payload
        self.client.publish(TOPIC_MANAGER, manager_msg)
        if self.source == "RGB":
            change_color(payload)
            
            
    def keepAlive(self):
        try:
            while True:
                current_time = time.time()
                uptime_seconds = int(current_time - self.start_time)
                massage = self.client_id + ": " + \
                str(uptime_seconds) + " seconds alive"
                self.client.publish(self.alive_topic, massage)
                manager_msg =  "keepalive"+ "/" + self.client_id + "/" + str(uptime_seconds) + " sec"
                self.client.publish(TOPIC_MANAGER, manager_msg )
                # Sleep for the keep-alive interval
                time.sleep(self.keep_alive_interval)
        except Exception as e:
            print(f"Error in keepAlive thread: {e}")
            
    def simulate_temperature_sensor(self, min_temp, max_temp, sleep):
        try:
            self.source = "temp"
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            while True:
                # Simulating temperature data
                temperature = random.randint(min_temp, max_temp)
                self.client.publish(self.topic, str(round(temperature, 2)))
                manager_msg =  self.source + "/" + self.client_id + "/" + str(round(temperature, 2))
                self.client.publish(TOPIC_MANAGER, manager_msg)
                time.sleep(sleep)  # Simulate sensor update interval
            alive_thread.join()
        except Exception as e:
            print(f"Error in temperature simulation: {e}")
            
    def simulate_humidity_sensor(self, min_temp, max_temp, sleep):
        try:
            self.source = "humidity"
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            while True:
                # Simulating humidity data
                humidity = random.randint(min_temp, max_temp)
                self.client.publish(self.topic, str(humidity))
                manager_msg =  self.source + "/" + self.client_id + "/" + str(humidity)
                self.client.publish(TOPIC_MANAGER, manager_msg)
                time.sleep(sleep)  # Simulate sensor update interval
            # alive_thread.join()
        except Exception as e:
            print(f"Error in humidity simulation: {e}")

    def simulate_rgb_sensor(self):
        try:
            self.source = "RGB"
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            create_RGB_led() # create the simulation
            alive_thread.join()
        except Exception as e:
            print(f"Error in RGB simulation: {e}")

    def simulate_doorLock_sensor(self):
        try:
            self.source = "DoorLock"
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            alive_thread.join()
        except Exception as e:
            print(f"Error in door lock simulation: {e}")

    def simulate_waterLevel_sensor(self, min_temp, max_temp, sleep):
        try:
            self.source = "waterLevel"
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            while True:
                # Simulating water data
                water = random.randint(min_temp, max_temp)
                self.client.publish(self.topic, str(water))
                manager_msg =  self.source + "/" + self.client_id + "/" + str(water)
                self.client.publish(TOPIC_MANAGER, manager_msg)
                time.sleep(sleep)  # Simulate sensor update interval
            alive_thread.join()
        except Exception as e:
            print(f"Error in water level simulation: {e}")

    def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            print(f"Error disconnecting from broker: {e}")
