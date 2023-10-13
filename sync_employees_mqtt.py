import os
from tinydb import TinyDB
import utils

data = {
    "doctype": "DTR Device",
    "serial_number": utils.get_serial(),
    "device_model": "esp8266"
}
employees = utils.get_all_employees(data)
utils.remove_temp_file()
db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
data = []
for employee in employees:
    user_id = employee[0]
    user_uid = employee[2]
    name = employee[1]
    rfid_number = employee[5]
    picture = employee[6]
    if employee[3] != 'Left':
        data.append({"user_id": user_id, 'user_uid': user_uid, 'name': name,
                     'attendance_device_id': rfid_number, 'picture': picture, 'company': employee[7]})

utils.save_employee_local(db, data)

for employee in db.all():
    frappe_client = utils.connect_erpnext(utils.config_server[employee['company']]['url'],
                                          utils.config_server[employee['company']]['username'],
                                          utils.config_server[employee['company']]['password'])

    picture = None
    if employee['picture'] and employee['picture'].find("http") != -1:
        picture = employee['picture']
    elif employee['picture']:
        picture = utils.config_server[employee['company']]['url'] + employee['picture']
    if picture:
        utils.download_image(picture, employee['user_id'], frappe_client)