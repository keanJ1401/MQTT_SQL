import paho.mqtt.client as mqtt
from models.handle_mqtt import *

mqtt_client = mqtt.Client(client_id="SQL_Handle", clean_session=True)

# Specify callback function
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.message_callback_add("+/mq2", mq2_handle)
mqtt_client.message_callback_add("+/bmp180", bmp180_handle)
mqtt_client.message_callback_add("+/si7021", si7021_handle)

# Establish a connection
mqtt_client.connect(host="192.168.0.101", port=1883, keepalive=60)
mqtt_client.loop_forever()



