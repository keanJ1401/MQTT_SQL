import paho.mqtt.client as mqtt

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('sensor/#')

# Message receiving callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.connect('192.168.0.101', 1883, 60)
client.loop_forever()