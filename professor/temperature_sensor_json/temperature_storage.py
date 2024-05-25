import paho.mqtt.client as mqtt
import json
import sqlite3
from sqlite3 import Error



# MQTT settings
mqtt_broker = "127.0.0.1"
mqtt_port = 1883
mqtt_topic = "house/temperature"

# SQLite settings
sqlite_db_file = "temperature.sqlite3"
sqlite_table = "temperature_data"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("house/temperature")

# Callback function for MQTT client
def on_message(client, userdata, msg):
    # Decode the received message
    data = json.loads(msg.payload.decode())

    # Store the data in SQLite database
    conn = sqlite3.connect(sqlite_db_file)
    
    sql = """INSERT INTO temperature_data (timestamp, temperature) VALUES (?, ?);"""
    params = (data["timestamp"], data["temperature"])

    try:
        c = conn.cursor()
        c.execute(sql, params)
  
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()
    

sql_create_coin_table = """
    CREATE TABLE IF NOT EXISTS temperature_data (
        id integer PRIMARY KEY,
        timestamp text NOT NULL,
        temperature text NOT NULL
    );
"""
conn = sqlite3.connect(sqlite_db_file)
try:
    c = conn.cursor()
    c.execute(sql_create_coin_table)
except Error as e:
    print(e)


# Connect to MQTT broker and subscribe to the topic
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_message = on_message
client.on_connect = on_connect
client.connect(mqtt_broker, mqtt_port)

# Start the MQTT client
client.loop_forever()