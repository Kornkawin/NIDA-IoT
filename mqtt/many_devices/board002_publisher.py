import numpy as np
import ssl
import time
import json
import paho.mqtt.client as mqtt
from config import *
from datetime import datetime

print("Running board002_publisher.py ...")
data = {'Device Name': 'board002', 'DateTime': '', 'Temperature': ''}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("factory/temperature_sensor")


def on_publish(client, userdata, rc):
    print("Published by", userdata, "result code " + str(rc))


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, userdata="boardLog002")
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.tls_set(ca_certs=ca_certificate,
                    certfile=client_certificates["board002"],
                    keyfile=client_keys["board002"], tls_version=ssl.PROTOCOL_SSLv23)
mqtt_client.tls_insecure_set(True)
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(host=mqtt_server_host,
                    port=mqtt_server_port,
                    keepalive=mqtt_keepalive)


if __name__ == '__main__':
    mqtt_client.loop_start()
    mu, sigma = 0, 1    # mean and standard deviation parameters
    while True:
        temperature = 37
        delta = np.random.normal(mu, sigma)
        temperature += delta
        print(temperature, delta)
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        data['DateTime'] = date_time_str
        data['Temperature'] = round(temperature, 2)
        data_json_str = json.dumps(data, indent=4)
        print(data_json_str)
        mqtt_client.publish("factory/temperature_sensor", data_json_str)
        time.sleep(1)
