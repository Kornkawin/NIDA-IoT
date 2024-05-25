import serial
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/sensor1")


def on_publish(client, userdata, rc):
    print("Published", userdata, " result code " + str(rc))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_publish = on_publish

if __name__ == '__main__':
    client.username_pw_set('pk', 'iot1234')

    #client.connect("127.0.0.1", 1883, 60)

    client.connect("192.168.1.39", 1883, 60)

    client.loop_start()

    # client.loop_forever()

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            client.publish("house/temperature", line.split()[-1])
