# print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import sys

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "edYgZ8epnXLPF95ROUMb"
forcing = "False"

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")
    temp_data = {'active': "false", 'force active': "Off"}
    client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)


def recv_message(client, userdata, message):
    global forcing
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'active': "true"}
    print(forcing)
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "Set motor" and jsonobj['params'] == "On":
            temp_data['active'] = "true"
            print(temp_data)
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        if jsonobj['method'] == "Set motor" and jsonobj['params'] == "Off":
            temp_data['active'] = "false"
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            print(temp_data)
        if jsonobj['method'] == "Force set motor" and jsonobj['params'] == "On":
            temp_data['force active'] = "On"
            forcing = "True"
            print(temp_data)
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        if jsonobj['method'] == "Force set motor" and jsonobj['params'] == "Off":
            temp_data['force active'] = "Off"
            forcing = "False"
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            print(temp_data)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")

client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message
while 1:
    time.sleep(1)