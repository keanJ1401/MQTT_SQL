import json
from models.model_sqlalchemy import *


# Connection success callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe("#")


# Message receiving callback
def on_message(client, userdata, msg):
    # payload = json.loads(msg.payload.decode('ascii')[:-1])
    # print(f"{msg.topic} {payload}")
    pass


# Sensors
def mq2_handle(client, userdata, msg):
    payload = json.loads(msg.payload.decode('ascii')[:-1])
    Sensors.add(7, payload, datetime.now())


def bmp180_handle(client, userdata, msg):
    payload = json.loads(msg.payload.decode('ascii')[:-1])
    Sensors.add(6, payload, datetime.now())


def si7021_handle(client, userdata, msg):
    payload = json.loads(msg.payload.decode('ascii')[:-1])
    Sensors.add(11, payload, datetime.now())


# Actuators
def light1_handle(client, userdata, msg):
    payload = str(msg.payload.decode('ascii')[:-1])
    Actuators.add(1, payload, datetime.now())


def light2_handle(client, userdata, msg):
    payload = str(msg.payload.decode('ascii')[:-1])
    Actuators.add(2, payload, datetime.now())


def door_handle(client, userdata, msg):
    payload = str(msg.payload.decode('ascii')[:-1])
    Actuators.add(3, payload, datetime.now())


def fan_handle(client, userdata, msg):
    payload = str(msg.payload.decode('ascii')[:-1])
    Actuators.add(4, payload, datetime.now())