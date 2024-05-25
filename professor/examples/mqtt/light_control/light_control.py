import paho.mqtt.client as mqtt
from gpiozero import LED
from time import sleep

led1 = LED(21)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/light1")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print(len(msg.payload))
    msg_str = msg.payload.decode("utf-8")
    # if msg.payload == bytearray('off'.encode()):
    if msg_str == 'OFF':
        print('Turn off')
        led1.off()
    elif msg_str == 'ON':
        print('Turn on')
        led1.on()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('pk', 'iot1234')

client.connect("127.0.0.1", 1883, 60)

client.loop_forever()
