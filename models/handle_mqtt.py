import json
from models.model_sqlalchemy import *


# Connection success callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe("sensor/#")


# Message receiving callback


def on_message(client, userdata, msg):
    # payload = json.loads(msg.payload.decode('ascii')[:-1])
    # print(f"{msg.topic} {payload}")
    pass


def mq2_handle(client, userdata, msg):
    payload = json.loads(msg.payload.decode('ascii')[:-1])
    Sensors.add(7, payload, datetime.now())


def bmp180_handle(client, userdata, msg):
    payload = json.loads(msg.payload.decode('ascii')[:-1])
    Sensors.add(6, payload, datetime.now())


def si7021_handle(client, userdata, msg):
    payload = json.loads(msg.payload.decode('ascii')[:-1])
    Sensors.add(11, payload, datetime.now())