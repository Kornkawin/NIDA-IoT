import paho.mqtt.client as mqtt
from gpiozero import LED, MotionSensor

led = LED(21)
pir = MotionSensor(11)
# enable sensor by default
pir.when_activated = led.on
pir.when_deactivated = led.off


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/light1")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print(len(msg.payload))
    msg_str = msg.payload.decode("utf-8")

    if msg_str == 'OFF':
        led.off()
        # enable sensor
        pir.when_activated = led.on
        pir.when_deactivated = led.off
    elif msg_str == 'ON':
        print('Turn on')
        led.on()
        # disable sensor
        pir.when_activated = None
        pir.when_deactivated = None


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.username_pw_set('iot', 'iot')
mqtt_client.connect("127.0.0.1", 1883, 60)
mqtt_client.loop_forever()
