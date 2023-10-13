import paho.mqtt.client as mqtt
from datetime import datetime
import json
import utils
from shutil import copyfile


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("tele/+/SENSOR")


def on_message(client, userdata, message):
    tmp_data = str(message.topic).split("/")
    device = str(tmp_data[1]).split("-")[0]
    payload = json.loads(message.payload)
    for key in utils.config.items('devices'):
        if str(key[0]).strip() == str(device).strip():
            now = datetime.now()
            data = {"date": now.strftime('%Y-%m-%d %H:%M:%S'), "direction": str(key[1]).strip(),
                    "device_id": device, "rfid_number": payload['decimal_code']}
            print("**********************************")
            print(data)
            print("**********************************")


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=str(utils.config.get("mqtt", "username")).strip(),
                           password=str(utils.config.get("mqtt", "password")).strip())
    client.connect(str(utils.config.get("mqtt", "url")).strip(), 1883, 60)
    client.loop_forever()
