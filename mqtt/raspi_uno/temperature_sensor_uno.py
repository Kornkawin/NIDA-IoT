"""
Read temperature from Arduino with the sensor by serial port and publish it to MQTT broker
"""

import json
import time
import serial
import paho.mqtt.client as mqtt
from config import *
from datetime import datetime

print("Running temperature_sensor_uno.py ...")
data = {'Device Name': 'temperature_real', 'DateTime': '', 'Temperature': ''}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/temp_sensor")


def on_publish(client, userdata, rc):
    print("Published by", userdata, "result code "+str(rc))


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, userdata="RealLogging")
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

if __name__ == '__main__':
    mqtt_client.username_pw_set(username, password)
    mqtt_client.connect(host=mqtt_server_host,
                        port=mqtt_server_port,
                        keepalive=mqtt_keepalive)
    mqtt_client.loop_start()
    ser = serial.Serial(serial_port, 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            temperature = line.split()[-1]

            try:
                temperature = float(temperature)
                temperature = round(temperature, 4)
            except ValueError:
                temperature = None

            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            data['DateTime'] = date_time_str
            data['Temperature'] = temperature
            data_json_str = json.dumps(data, indent=4)
            print(data_json_str)
            mqtt_client.publish("house/temp_sensor", data_json_str)
            time.sleep(1)
