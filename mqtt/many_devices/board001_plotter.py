import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import ssl
import time
import json
from config import *

print("Running board001_plotter.py ...")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("factory/temperature_sensor")


# Define the callback function for when the MQTT client receives a message
def on_message(client, userdata, msg):
    print(msg.topic, str(msg.payload))
    msg_str = msg.payload.decode("utf-8")
    msg = json.loads(msg_str)
    print('Received', msg)
    # Append the temperature value to the list of data
    if msg['Device Name'] == 'board002':
        data002.append(msg['Temperature'])
    elif msg['Device Name'] == 'board003':
        data003.append(msg['Temperature'])


# Create an MQTT client and connect to the broker
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(ca_certs=ca_certificate,
                    certfile=client_certificates["board001"],
                    keyfile=client_keys["board001"], tls_version=ssl.PROTOCOL_SSLv23)
mqtt_client.tls_insecure_set(True)
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(host=mqtt_server_host,
                    port=mqtt_server_port,
                    keepalive=mqtt_keepalive)

# Initialize an empty list to store the temperature data
data002 = []
data003 = []

# Initialize the plot with 2 empty lines
plt.ion()
plt.show()


if __name__ == '__main__':
    # Start the MQTT client loop and wait for incoming messages
    mqtt_client.loop_start()

    # Keep the program running indefinitely
    while True:
        # Update the plot with the new data
        plt.clf()
        plt.plot(data002, label='board002')
        plt.plot(data003, label='board003')
        plt.legend()
        plt.title("Temperature Sensor Data")
        plt.xlabel("Time (ticks)")
        plt.ylabel("Temperature (°C)")
        plt.grid()
        plt.draw()
        plt.pause(1)
        time.sleep(5)
