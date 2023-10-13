import json
import utils
import paho.mqtt.client as mqtt
from tinydb import TinyDB, Query
import os

conn = None

try:
    db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
    conn = utils.zk.connect()
    conn.disable_device()
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            pass
        else:
            employee = {"uid": attendance.uid, "user_id": attendance.user_id,
                        "date": attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        "punch": attendance.punch, "status": attendance.status}

            rfid = ""
            Employee = Query()
            result = db.search(Employee.user_id == attendance.user_id)
            if result:
                rfid = result[0]['attendance_device_id']

            data = {"device_id": conn.get_serialnumber(), "hex_code": rfid, "raw": employee}
            json_str = str(json.dumps(data)).strip()
            if json_str:
                topic = "tele/{}/SENSOR".format(utils.get_serial())
                client = mqtt.Client()
                client.username_pw_set(username=str(utils.config.get("mqtt", "username")).strip(),
                                       password=str(utils.config.get("mqtt", "password")).strip())
                client.connect(str(utils.config.get("mqtt", "url")).strip(), 1883, 60)
                client.publish(topic, json_str)

    conn.enable_device()
except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
