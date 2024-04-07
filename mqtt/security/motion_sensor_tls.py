import paho.mqtt.client as mqtt
import ssl
import datetime
import json
from config import *
from gpiozero import MotionSensor, LED

print("Running motion_sensor_tls.py ...")
PIR1 = MotionSensor(4)
LED1 = LED(16)
data = {'Device Name': 'Board001', 'DateTime': '', 'Status': 'DEACTIVATED'}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/motion_sensor")


def on_publish(client, userdata, rc):
    print("Published by", userdata, "result code "+str(rc))


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, userdata="AtomHouse")
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish


def motion_activated():
    data['DateTime'] = str(datetime.datetime.now())
    data['Status'] = 'ACTIVATED'
    message = json.dumps(data)
    mqtt_client.publish("house/motion_sensor", message)
    LED1.on()


def motion_deactivated():
    data['DateTime'] = str(datetime.datetime.now())
    data['Status'] = 'DEACTIVATED'
    message = json.dumps(data)
    mqtt_client.publish("house/motion_sensor", message)
    LED1.off()


PIR1.when_activated = motion_activated
PIR1.when_deactivated = motion_deactivated
mqtt_client.tls_set(ca_certs=ca_certificate,
                    certfile=client_certificate,
                    keyfile=client_key, tls_version=ssl.PROTOCOL_SSLv23)
mqtt_client.tls_insecure_set(True)
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(host=mqtt_server_host,
                    port=mqtt_server_port,
                    keepalive=mqtt_keepalive)
mqtt_client.loop_forever()
