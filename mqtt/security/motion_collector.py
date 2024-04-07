import paho.mqtt.client as mqtt
import ssl
import json
from config import *
from motion_db import MotionSensor, create_connection

print("Running motion_collector.py ...")
DATABASE = 'motion_data.sqlite3'
cnx = create_connection(DATABASE)
MotionSensor.setup(cnx)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/motion_sensor")


def on_publish(client, userdata, rc):
    print("Published", userdata, " result code "+str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    msg_str = msg.payload.decode("utf-8")
    msg = json.loads(msg_str)
    motion_sensor = MotionSensor(device_name=msg['Device Name'], timestamp=msg['DateTime'], status=msg['Status'])
    MotionSensor.insert(motion_sensor)


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, userdata="AtomLogging")
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_message = on_message
mqtt_client.tls_set(ca_certs=ca_certificate,
                    certfile=client_certificate,
                    keyfile=client_key, tls_version=ssl.PROTOCOL_SSLv23)
mqtt_client.tls_insecure_set(True)
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(host=mqtt_server_host,
                    port=mqtt_server_port,
                    keepalive=mqtt_keepalive)
mqtt_client.loop_forever()
