print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "U4ugcpWt538wp5AwVGJ0"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
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

f = open(r'C:\Users\hatru\OneDrive\Desktop\data\tram_1.txt','r')
while f:
    data = f.readline().replace('\n', '')
    t = data.split(";")
    m = "{"
    for x in range(len(t) - 1):
        t1 = t[x].split(',')
        if x != len(t) - 1 and x != 0:
            m = m + ", ";
        if len(t1) > 1:
            m = m + '"' + t1[0] + '"' + ': ' + '"' + t1[1] + '"'
        else:
            if t1[0].find(':') != -1:
                m = m + '"Hour": '
            else:
                m = m + '"Date": '
            m += '"' + t1[0] + '"'
    m+="}"
    #print(m)
    client.publish('v1/devices/me/telemetry', m, 1)
    time.sleep(5)




