from gpiozero import MotionSensor, LED
from signal import pause
import paho.mqtt.client as mqtt
import ssl
from config import *


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/sensor1")


def on_publish(client, userdata, rc):
    print("Published", userdata, " result code "+str(rc))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_publish = on_publish


def motion_activated():
    client.publish("house/motion_sensor", "ACTIVATED")
    led.on()


def motion_deactivated():
    client.publish("house/motion_sensor", "DEACTIVATED")
    led.off()


pir = MotionSensor(4)
led = LED(16)

pir.when_activated = motion_activated
pir.when_deactivated = motion_deactivated

client.tls_set(ca_certs=ca_certificate,
               tls_version=ssl.PROTOCOL_SSLv23, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.username_pw_set(username, password)

client.connect(host=mqtt_server_host,
               port=mqtt_server_port,
               keepalive=mqtt_keepalive)


client.loop_start()

client.loop_forever()
