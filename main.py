# print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "PkSXWNyACzrxEtvM9Blv"


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

f = open("./data/tram_1.txt", "r")
while f:
    data = f.readline().replace('\n', '')
    t = data.split(";")
    # m = "{"
    entry_dict = {
            "SEQ": "",
            "STT": "",
            "Hour": "",
            "Date": "",
            "pH": "",
            # "PH": "",
            # "COLOR": "",
            "Color": "",
            #"FLOW"
            "Flow": "",
            # "FLOW": "",
            "TSS": "",
            # "TEMP": "",
            "temperature": "",
            "COD": "",
            "CLO": "",
            "SS": "",
            "TN": "",
            "NH4": "",
            "N-NH4": "",
            "N-NH4+": "",
            "MO": "",
            "VBAT": "",
            "VDDA": "",
            "INTEMP": "",
        }
    for x in range(len(t) - 1):
        t1 = t[x].split(',')
        # if x != len(t) - 1 and x != 0:
        #     m = m + ", "
        if len(t1) > 1:
            # m = m + '"' + t1[0] + '"' + ': ' + '"' + t1[1] + '"'
            if t1[0] == "COLOR":
                entry_dict["Color"] = t1[1]
            elif t1[0] == "PH":
                entry_dict["pH"] = t1[1]
            elif t1[0] == "FLOW":
                entry_dict["Flow"] = t1[1]
            elif t1[0] == "TEMP" or t1[0] == "Temp":
                entry_dict["temperature"] = t1[1]
            else:
                entry_dict[t1[0]] = t1[1]
        else:
            if t1[0].find(':') != -1:
                # m = m + '"Hour": '
                entry_dict["Hour"] = t1[0]
            else:
            #     m = m + '"Date": '
            # m += '"' + t1[0] + '"'
                entry_dict["Date"] = t1[0]

    # m+="}"
    print(json.dumps(entry_dict))
    client.publish('esp/telemetry', json.dumps(entry_dict), 1)
    time.sleep(5)




