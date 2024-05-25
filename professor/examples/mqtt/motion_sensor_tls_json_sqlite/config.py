import os.path

certificates_path = "/Users/pramote/workspace/iot/mqtt/mosquitto_certificates"
ca_certificate = os.path.join(certificates_path, "ca.crt")
client_certificate = os.path.join(certificates_path, "board001.crt")
client_key = os.path.join(certificates_path, "board001.key")

mqtt_server_host = "192.168.1.35"
mqtt_server_port = 8883
mqtt_keepalive = 60
username = 'pk'
password = 'iot123'
