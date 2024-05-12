import paho.mqtt.client as mqtt
import ssl
import json
from config import *
from temperature_db import TemperatureSensor, create_connection

print("Running board001_collector.py ...")
DATABASE = 'temperature_sensor.sqlite3'
cnx = create_connection(DATABASE)
TemperatureSensor.setup(cnx)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("factory/temperature_sensor")


def on_publish(client, userdata, rc):
    print("Published by", userdata, "result code "+str(rc))


def on_message(client, userdata, msg):
    print(msg.topic, str(msg.payload))
    msg_str = msg.payload.decode("utf-8")
    msg = json.loads(msg_str)
    temp_sensor = TemperatureSensor(device_name=msg['Device Name'], timestamp=msg['DateTime'], temperature=msg['Temperature'])
    TemperatureSensor.insert(temp_sensor)


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, userdata="boardLog001")
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_message = on_message
mqtt_client.tls_set(ca_certs=ca_certificate,
                    certfile=client_certificates["board001"],
                    keyfile=client_keys["board001"], tls_version=ssl.PROTOCOL_SSLv23)
mqtt_client.tls_insecure_set(True)
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(host=mqtt_server_host,
                    port=mqtt_server_port,
                    keepalive=mqtt_keepalive)


if __name__ == '__main__':
    mqtt_client.loop_forever()
