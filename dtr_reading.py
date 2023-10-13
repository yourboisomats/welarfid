import os
from tinydb import TinyDB, Query
import json
import utils
import datetime

conn = None
import paho.mqtt.client as mqtt

def zk_device_info(device):
    return {'get_firmware_version': device.get_firmware_version(),
            'serial_number': device.get_serialnumber(),
            'platform': device.get_platform(),
            'device_name': device.get_device_name(),
            'face_version': device.get_face_version(),
            'fp_version': device.get_fp_version(),
            'extend_fmt': device.get_extend_fmt(),
            'user_extend_fmt': device.get_user_extend_fmt(),
            'face_fun_on': device.get_face_fun_on(),
            'compat_old_firmware': device.get_compat_old_firmware(),
            'network_params': device.get_network_params(),
            'mac': device.get_mac(),
            'pin_width': device.get_pin_width()
            }


def get_employee_zk(device):
    users = device.get_users()
    data = []
    for user in users:
        data.append(
            {"user_id": user.user_id, 'user_uid': user.uid, 'name': user.name,
             'attendance_device_id': user.card, 'company': user.group_id, "picture": ""})
    return data


conn = utils.zk.connect()
conn.disable_device()
device_info = zk_device_info(conn)
db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')

attendances = conn.get_attendance()
count = 0
for attendance in attendances:
    date1 = datetime.datetime.strftime(datetime.date.today(), "%Y-%m")
    date2 = datetime.datetime.strftime(attendance.timestamp, "%Y-%m")
    if date1.strip() == date2.strip():
        employee = {"uid": attendance.uid, "user_id": attendance.user_id,
                    "date": attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    "punch": attendance.punch, "status": attendance.status}

        rfid = ""
        Employee = Query()
        result = db.search(Employee.user_id == attendance.user_id)
        if result:
            rfid = result[0]['attendance_device_id']

        data = {"device_id": conn.get_serialnumber(), "hex_code": rfid, "raw": employee, "re_upload": 1}
        json_str = str(json.dumps(data)).strip()
        if json_str:
            topic = "tele/{}/SENSOR".format(utils.get_serial())
            client = mqtt.Client()
            client.username_pw_set(username=str(utils.config.get("mqtt", "username")).strip(),
                                   password=str(utils.config.get("mqtt", "password")).strip())
            client.connect(str(utils.config.get("mqtt", "url")).strip(), 1883, 60)
            client.publish(topic, json_str)
        count += 1
conn.clear_attendance()
conn.enable_device()
if conn:
    conn.disconnect()

print(str(count) + ' of attendance uploaded')
