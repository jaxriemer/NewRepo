import time
import board
import busio
import qwiic_button

import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/nek/button'

i2c = busio.I2C(board.SCL, board.SDA)
button = qwiic_button.QwiicButton()
button.begin()

while True:
    for i in range(12):
        if button.is_button_pressed():
            val = "button pressed"
            print(val)
            client.publish(topic, val)
    time.sleep(0.25)
