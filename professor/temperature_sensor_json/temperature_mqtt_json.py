import numpy as np
import time
import datetime
import json
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/sensor1")


def on_publish(client, userdata, rc):
    print("Published", userdata, " result code " + str(rc))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_publish = on_publish

if __name__ == '__main__':
    client.username_pw_set('pk', 'iot1234')

    client.connect("127.0.0.1", 1883, 60)

    #client.connect("192.168.1.39", 1883, 60)

    client.loop_start()

    # client.loop_forever()

    mu, sigma = 0, 1 # mean and standard deviation
    temperature = 37
    while True:
        delta = np.random.normal(mu, sigma)
        temperature += delta
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {'timestamp': date_time_str, 'temperature': temperature}
        data_json_str = json.dumps(data, indent=4)
        print(data_json_str)
        client.publish("house/temperature", data_json_str)
        time.sleep(1)
