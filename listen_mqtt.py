import paho.mqtt.client as mqtt
from datetime import datetime
import json
import utils
from shutil import copyfile
import os
from tinydb import TinyDB


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("tele/+/SENSOR")


def on_message(client, userdata, message):
    tmp_data = str(message.topic).split("/")
    device = str(tmp_data[1]).split("-")[0]
    payload = json.loads(message.payload)

    db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
    employees = db.all()
    for employee in employees:
        if employee['attendance_device_id']:
            if 're_upload' in payload:
                re_upload = True
            else:
                re_upload = False

            if str(payload['hex_code']).strip() in str(employee['attendance_device_id']):
                client.publish("cmnd/" + device + "/POWER", json.dumps({"status": "ON"}))
                try:
                    key = utils.find_device(device)
                    now = datetime.now()
                    data = {"date": payload['raw']['date'], "direction": str(key[1]).strip(),
                            "device_id": device, "rfid_number": payload['hex_code'], "raw": payload}
                    date_time = now.strftime("%Y%d%m@%H:%M:%S")
                    employee_json = json.dumps(data)
                    file_name = utils.path_name + '/data/' + date_time + '@' + str(payload['hex_code']) + '@' + device
                    if not re_upload and str(utils.config.get("sms", "enable")) == str(1):
                        f = open(file_name + ".sms", "w+")
                        f.write(employee_json)
                        f.close()
                    if re_upload:
                        f = open(file_name + ".data", "w+")
                        f.write(employee_json)
                        f.close()
                except:
                    None
    db.close()

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=str(utils.config.get("mqtt", "username")).strip(),
                           password=str(utils.config.get("mqtt", "password")).strip())
    client.connect(str(utils.config.get("mqtt", "url")).strip(), 1883, 60)
    client.loop_forever()
