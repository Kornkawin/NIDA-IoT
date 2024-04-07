from tkgpio import TkCircuit

# initialize the circuit inside the GUI
configuration = {
    "width": 300,
    "height": 300,
    "leds": [
        {"x": 50, "y": 40, "name": "LED", "pin": 21},
    ],
    "motion_sensors": [
        {"x": 50, "y": 200, "name": "Motion Sensor", "pin": 11,
            "detection_radius": 50, "delay_duration": 5, "block_duration": 3}
    ],
}

circuit = TkCircuit(configuration)


@circuit.run
def main():
    import light_control
