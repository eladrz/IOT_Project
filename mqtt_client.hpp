#ifndef MQTT_CLIENT_HPP
#define MQTT_CLIENT_HPP

#include <iostream>
#include <cstring>
#include <mosquitto.h>

class MQTT_Client {
public:
    MQTT_Client();
    ~MQTT_Client();

    bool connect(const char* host, int port, int keepalive);
    bool publish(const char* topic, const char* payload);
    bool subscribe(const char* topic);
    bool loop();

private:
    struct mosquitto *mosq;

    static void on_message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message);
};

#endif // MQTT_CLIENT_HPP

