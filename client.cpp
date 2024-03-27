#include "mqtt_client.hpp"
#include <iostream>
#include <cstring>
//to compile: g++ client.cpp mqtt_client.cpp -o mqtt_client -lmosquitto
#define TOPIC "test/A"


int main() {
    MQTT_Client client;
    if (client.connect("localhost", 1883, 60)) {
    	  std::string Smessage = "I am up! my topic is: " + std::string(TOPIC);
        client.subscribe(TOPIC);
        client.publish(TOPIC,  Smessage.c_str());
        });
        while (client.loop()) {
            // Continue processing MQTT messages
        }
    } else {
        std::cerr << "Failed to connect to MQTT broker." << std::endl;
        return 1;
    }

    return 0;
}

