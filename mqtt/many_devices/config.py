import os.path
import pathlib

current_path = pathlib.Path().resolve()
certificates_path = os.path.join(current_path, "mosquitto_certificates")
ca_certificate = os.path.join(certificates_path, "ca.crt")
client_certificates = {
    "board001": os.path.join(certificates_path, "board001.crt"),
    "board002": os.path.join(certificates_path, "board002.crt"),
    "board003": os.path.join(certificates_path, "board003.crt"),
}
client_keys = {
    "board001": os.path.join(certificates_path, "board001.key"),
    "board002": os.path.join(certificates_path, "board002.key"),
    "board003": os.path.join(certificates_path, "board003.key"),
}

mqtt_server_host = "127.0.0.1"
mqtt_server_port = 8883
mqtt_keepalive = 60
username = "iot123"
password = "iot123"
