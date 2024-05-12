import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import time
import json
from config import *

print("Running temperature_plotter.py ...")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/temp_sensor")


# Define the callback function for when the MQTT client receives a message
def on_message(client, userdata, msg):
    print(msg.topic, str(msg.payload))
    msg_str = msg.payload.decode("utf-8")
    msg = json.loads(msg_str)
    print('Received', msg)
    # Append the temperature value to the list of data
    data.append(msg['Temperature'])


# Create an MQTT client and connect to the broker
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(host=mqtt_server_host,
                    port=mqtt_server_port,
                    keepalive=mqtt_keepalive)

# Initialize an empty list to store the temperature data
data = []

# Initialize the plot with an empty line
plt.ion()
plt.show()
plt.plot(data)

# Start the MQTT client loop and wait for incoming messages
mqtt_client.loop_start()

# Keep the program running indefinitely
while True:
    # Update the plot with the new data
    plt.clf()
    plt.plot(data)
    plt.draw()
    plt.pause(0.001)
    time.sleep(5)
