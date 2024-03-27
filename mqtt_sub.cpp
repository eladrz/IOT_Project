#include <iostream>
#include <cstring>
#include <mosquitto.h>
//g++ mqttSub.cpp -o mqtt_subscriber -lmosquitto

#define MQTT_HOST "localhost"  // Change this to your MQTT broker address
#define MQTT_PORT 1883         // Change this to your MQTT broker port

// Callback function for handling MQTT messages
void on_message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message) {
    if (message->payloadlen) {
    	  const char *payload_str = (const char *)message->payload;
        std::cout << "Received message on topic '" << message->topic << "': " << payload_str << std::endl;
    } else {
        std::cout << "Empty message received on topic '" << message->topic << "'!" << std::endl;
    }
}

int main() {
    // Initialize Mosquitto library
    mosquitto_lib_init();

    // Create a new MQTT client instance
    struct mosquitto *mosq = mosquitto_new(NULL, true, NULL);
    if (!mosq) {
        std::cerr << "Error: Unable to create MQTT client instance." << std::endl;
        return 1;
    }

    // Set up MQTT message callback
    mosquitto_message_callback_set(mosq, on_message_callback);

    // Connect to MQTT broker
    int ret = mosquitto_connect(mosq, MQTT_HOST, MQTT_PORT, 60);
    if (ret != MOSQ_ERR_SUCCESS) {
        std::cerr << "Unable to connect to MQTT broker. Error code: " << ret << std::endl;
        mosquitto_destroy(mosq);
        mosquitto_lib_cleanup();
        return 1;
    }

    // Subscribe to all topics
    ret = mosquitto_subscribe(mosq, NULL, "#", 0);
    if (ret != MOSQ_ERR_SUCCESS) {
        std::cerr << "Error subscribing to all topics. Error code: " << ret << std::endl;
        mosquitto_destroy(mosq);
        mosquitto_lib_cleanup();
        return 1;
    }

    // Loop and handle MQTT messages
    while (true) {
        ret = mosquitto_loop(mosq, -1, 1);
        if (ret) {
            std::cerr << "Error in MQTT loop. Error code: " << ret << std::endl;
            break;
        }
    }

    // Clean up
    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();

    return 0;
}

