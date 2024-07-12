import time
import random
import paho.mqtt.client as mqtt
import threading
import tkinter as tk

import guiSensors
from guiSensors import *
import json


class SensorClient:
    def __init__(self, client_id, broker_address, topic, alive_topic, keep_alive_interval, username=None,
                 password=None):
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

    def connect(self):
        try:
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.broker_address)
            if self.topic == "DoorLock":
                guiSensors.get_sensor_client(self)
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
        try:
            # handle the simulation
            msgTopic = msg.topic
            payload = msg.payload.decode('utf-8')
            jsonMsg = json.loads(payload)
            if msgTopic == "RGB":
                if jsonMsg['payload'] == 'off':
                    turn_off(self)
                elif jsonMsg['payload'] == 'on':
                    turn_on(self)
                else:
                    change_color_from_msg(jsonMsg['payload'])

            elif msgTopic == "DoorLock":
                check_signal(jsonMsg['payload'])
        except Exception as e:
            print(f"Exception: {e}")

    def keepAlive(self):
        try:
            while True:
                current_time = time.time()
                uptime_seconds = int(current_time - self.start_time)
                msg = {
                    'sys_id': self.client_id,
                    'device': self.topic,
                    'payload': str(uptime_seconds) + " sec"
                }
                json_message = json.dumps(msg)
                self.client.publish('keepalive', json_message)
                # Sleep for the keep-alive interval
                time.sleep(self.keep_alive_interval)
        except Exception as e:
            print(f"Error in keepAlive thread: {e}")

    def simulate_temperature_sensor(self, min_temp, max_temp, sleep):
        try:
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            while True:
                # Simulating temperature data
                temperature = random.randint(min_temp, max_temp)
                msg = {
                    'sys_id': self.client_id,
                    'payload': temperature
                }
                json_message = json.dumps(msg)
                self.client.publish(self.topic, json_message)
                time.sleep(sleep)  # Simulate sensor update interval
            alive_thread.join()
        except Exception as e:
            print(f"Error in temperature simulation: {e}")

    def simulate_humidity_sensor(self, min_temp, max_temp, sleep):
        try:
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            while True:
                # Simulating humidity data
                humidity = random.randint(min_temp, max_temp)
                msg = {
                    'sys_id': self.client_id,
                    'payload': humidity
                }
                json_message = json.dumps(msg)
                self.client.publish(self.topic, json_message)
                time.sleep(sleep)  # Simulate sensor update interval
            alive_thread.join()
        except Exception as e:
            print(f"Error in humidity simulation: {e}")

    def simulate_rgb_sensor(self):
        try:
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            create_RGB_led(self)  # create the simulation
            alive_thread.join()
        except Exception as e:
            print(f"Error in RGB simulation: {e}")

    def simulate_doorLock_sensor(self):
        try:
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            DoorLock_Simulation()  # simulation of door lock
            alive_thread.join()
        except Exception as e:
            print(f"Error in door lock simulation: {e}")

    def simulate_waterLevel_sensor(self, min_temp, max_temp, sleep):
        try:
            alive_thread = threading.Thread(target=self.keepAlive)
            alive_thread.start()
            while True:
                # Simulating water data
                water = random.randint(min_temp, max_temp)
                msg = {
                    'sys_id': self.client_id,
                    'payload': water
                }
                json_message = json.dumps(msg)
                self.client.publish(self.topic, json_message)
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
