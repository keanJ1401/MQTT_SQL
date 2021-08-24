import paho.mqtt.client as mqtt
from models.handle_mqtt import *

mqtt_client = mqtt.Client(client_id="SQL_Handle", clean_session=True)

# Specify callback function
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Callback for every topic
mqtt_client.message_callback_add("+/mq2", mq2_handle)
mqtt_client.message_callback_add("+/bmp180", bmp180_handle)
mqtt_client.message_callback_add("+/si7021", si7021_handle)
mqtt_client.message_callback_add("+/max44009", max44009_handle)
mqtt_client.message_callback_add("+/light1", light1_handle)
mqtt_client.message_callback_add("+/light2", light2_handle)
mqtt_client.message_callback_add("+/door/control", door_control_handle)
mqtt_client.message_callback_add("+/door/mode", door_mode_handle)
mqtt_client.message_callback_add("+/fan", fan_handle)

# Establish a connection
mqtt_client.connect(host="localhost", port=1883, keepalive=60)
mqtt_client.loop_forever()



