import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import time
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/temperature")


# Define the callback function for when the MQTT client receives a message
def on_message(client, userdata, msg):
    # Decode the message payload as a float value
    info = json.loads(msg.payload.decode())
    temp = float(info['temperature'])
    print('Received', temp)
    # Append the temperature value to the list of data
    data.append(temp)



# Create an MQTT client and connect to the broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883)

# # Subscribe to the topic that publishes temperature data
# client.subscribe("house/temperature")

# Initialize an empty list to store the temperature data
data = []

# Initialize the plot with an empty line
plt.ion()
plt.show()
plt.plot(data)

# Start the MQTT client loop and wait for incoming messages
client.loop_start()

# Keep the program running indefinitely
while True:
        # Update the plot with the new data
    plt.clf()
    plt.plot(data)
    plt.draw()
    plt.pause(0.001)
    time.sleep(5)
