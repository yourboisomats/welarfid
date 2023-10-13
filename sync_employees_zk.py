from zk import ZK, const
import os
from tinydb import TinyDB, Query
import json
import utils

conn = None


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

data = {
    "doctype": "DTR Device",
    "serial_number": device_info['serial_number'],
    "device_name": device_info['device_name'],
    "device_data": json.dumps(device_info)
}

employees = utils.get_all_employees(data)

utils.remove_temp_file()
db = TinyDB(os.path.abspath(utils.path_name) + '/tmp.json')

utils.save_employee_local(db, get_employee_zk(conn))
Employee = Query()
print("******************************")
print("Sync Employees")
print("******************************")
print("")
for employee in employees:
    print("================================")
    print(employee)
    if employee[3] != 'Left':
        result = db.search(Employee.user_id == employee[0])
        if employee[2]:
            uid = int(employee[2])
        else:
            uid = 0
        if result:
            if result[0]['user_uid'] != employee[2]:
                conn.delete_user(user_id=employee[0])

        result = db.search(Employee.uid == uid)
        if result:
            if result[0]['user_id'] != employee[0]:
                print("delete not the same user_id")
                conn.delete_user(uid=uid)
        if employee[5]:
            rfid = employee[5]
        else:
            rfid = 0
        if employee[1] and employee[0]:
            try:
                print("updating/adding user")
                conn.set_user(uid=uid, name=employee[1], privilege=const.USER_DEFAULT, password='12345678',
                              group_id="0", user_id=employee[0], card=rfid)
            except Exception as e:
                print(e)
    else:
        try:
            print("delete not in the company")
            conn.delete_user(user_id=employee[0])
        except:
            None

utils.remove_temp_file()
employees_db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
utils.save_employee_local(employees_db, get_employee_zk(conn))
conn.enable_device()
if conn:
    conn.disconnect()

print("******************************")
print("Downloading images")
print("******************************")
print("")
for employee in employees:
    result = db.search(Employee.user_id == employee[0])
    if result:
        if employee[6]:
            print("===============================")
            print(employee[1])
            print(employee[6])
            print(employee)
            frappe_client = utils.connect_erpnext(utils.config_server[employee[7]]['url'],
                                                  utils.config_server[employee[7]]['username'],
                                                  utils.config_server[employee[7]]['password'])
            result[0]['company'] = employee[7]
            result[0]['picture'] = employee[6]

            image = ""
            if 'http' in str(employee[6]):
                image = str(employee[6])
            else:
                image = utils.config_server[employee[7]]['url'] + '/' + str(employee[6])
            print(image)

            employees_db.upsert(result[0], Employee.user_id == result[0]['user_id'])
            utils.download_image(image, employee[0], frappe_client)
