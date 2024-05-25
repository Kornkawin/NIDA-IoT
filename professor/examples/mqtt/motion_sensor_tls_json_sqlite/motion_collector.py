import paho.mqtt.client as mqtt
import ssl
import datetime
import json
import sqlite3

from config import *
from motion_db import MotionSensor
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/motion_sensor")


def on_publish(client, userdata, rc):
    print("Published", userdata, " result code "+str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    msg_str = msg.payload.decode("utf-8")
    msg = json.loads(msg_str)
    motion_sensor = MotionSensor(device_name=msg['Device Name'],
                                 timestamp=msg['DateTime'], status=msg['Status'])
    MotionSensor.insert(motion_sensor)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message


def create_connection(database):
    cnx = None
    try:
        cnx = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(e)
    return cnx


client.tls_set(ca_certs=ca_certificate,
               certfile=client_certificate,
               keyfile=client_key, tls_version=ssl.PROTOCOL_SSLv23)

client.tls_insecure_set(True)
client.username_pw_set(username, password)

client.connect(host=mqtt_server_host,
               port=mqtt_server_port,
               keepalive=mqtt_keepalive)


client.loop_start()
database = 'motion_data.sqlite3'
cnx = create_connection(database)
MotionSensor.setup(cnx)


# while True:
#     time.sleep(1)

client.loop_forever()
