import configparser
import sys
import os
from frappeclient import FrappeClient
from zk import ZK, const
import shutil

path_name = os.path.dirname(sys.argv[0])
path = os.path.abspath(path_name)
config_path = os.path.abspath(path_name) + "/device.cfg"
config = configparser.ConfigParser()
config.optionxform = str
config.read(config_path)

config_sever_path = os.path.abspath(path_name) + "/server.cfg"
config_server = configparser.ConfigParser()
config_server.optionxform = str
config_server.read(config_sever_path)

zk = ZK(str(config.get("zkteco", "ip")).strip(), port=int(str(config.get("zkteco", "port")).strip()), timeout=5,
        password=0, force_udp=False, ommit_ping=False)


def connect_erpnext(url, user_name, password):
    return FrappeClient(url, user_name, password)


def get_serial():
    cpu_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = "ERROR000000000"
    return cpu_serial


def update_esp8266():
    data_esp8266 = {
        "doctype": "DTR Device",
        "serial_number": get_serial(),
        "device_model": "esp8266"
    }
    update_device(data_esp8266)


def get_all_employees(device_data):
    employees = []
    sections = config_server.sections()
    for section in sections:
        frappe_client = connect_erpnext(config_server[section]['url'],
                                        config_server[section]['username'],
                                        config_server[section]['password'])
        company_employees = get_employees_from_erpnext(frappe_client)
        for employee in company_employees:
            employee.append(section)
            if employee[2]:
                employee[2] = int(employee[2]) + int(config_server[section]['uid'])
            employees.append(employee)
        update_device(device_data, frappe_client)
    return employees


def find_device(device):
    for key in config.items('devices'):
        if str(key[0]).strip() == str(device).strip():
            return key

    return ['None', 'None']


def update_device(data, frappe_client):
    try:
        result = frappe_client.get_doc("DTR Device", data['serial_number'])
        result['status'] = 'Online'
        frappe_client.update(result)
    except:
        result = frappe_client.insert(data)
    return result


def save_attendance(data, frappe_client):
    frappe_client.insert(data)


def remove_temp_file():
    try:
        os.remove(os.path.abspath(path_name) + '/employees.json')
        os.remove(os.path.abspath(path_name) + '/tmp.json')
    except:
        None


def get_employees_from_erpnext(frappe_client):
    return frappe_client.get_api("payroll.rest.employee_data_device")


def save_employee_local(local_db, employees):
    for employee in employees:
        local_db.insert({'user_uid': employee['user_uid'], 'user_id': employee['user_id'], 'name': employee['name'],
                         'attendance_device_id': employee['attendance_device_id'],
                         'company': employee['company'], 'picture': employee['picture']})


def download_image(picture, user_id, frappe_client):
    if picture:
        try:
            filename, file_extension = os.path.splitext(picture)
            image_file = os.path.abspath(path_name) + '/images/' + user_id + file_extension
            r = frappe_client.session.get(str(picture), stream=True)
            if r.status_code == 200:
                print("success")
                print(image_file)
                with open(image_file, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except:
            None
