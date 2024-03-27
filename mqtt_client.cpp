#include "mqtt_client.hpp"

MQTT_Client::MQTT_Client() 
{
    mosquitto_lib_init();
    mosq = mosquitto_new(NULL, true, NULL);
    if (!mosq)
    {
        std::cerr << "Error: Unable to create MQTT client instance." << std::endl;
    }
    mosquitto_message_callback_set(mosq, on_message_callback);
}

MQTT_Client::~MQTT_Client() {
    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();
}

bool MQTT_Client::connect(const char* host, int port, int keepalive) {
    int ret = mosquitto_connect(mosq, host, port, keepalive);
    return ret == MOSQ_ERR_SUCCESS;
}

bool MQTT_Client::publish(const char* topic, const char* payload) {
    int ret = mosquitto_publish(mosq, NULL, topic, strlen(payload), payload, 0, false);
    return ret == MOSQ_ERR_SUCCESS;
}

bool MQTT_Client::subscribe(const char* topic) {
    int ret = mosquitto_subscribe(mosq, NULL, topic, 0);
    return ret == MOSQ_ERR_SUCCESS;
}

bool MQTT_Client::loop() {
    int ret = mosquitto_loop(mosq, -1, 1);
    return ret == MOSQ_ERR_SUCCESS;
}

void MQTT_Client::on_message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message) {
    if (message->payloadlen) {
        std::cout << "Received message: " << (char *)message->payload << std::endl;
    } else {
        std::cout << "Empty message received!" << std::endl;
    }
}

