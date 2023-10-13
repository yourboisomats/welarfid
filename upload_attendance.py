import utils
import glob
import json
from tinydb import TinyDB, Query
import os


def upload_data():
    Employee = Query()
    db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
    device_id = utils.get_serial()
    for log in glob.glob(utils.path + "/data/*" + ".data"):
        with open(log) as json_file:
            try:
                data = json.load(json_file)
                result = db.search(Employee.attendance_device_id == str(data['rfid_number']).strip())
                if len(result) > 0:
                    data = {
                        "doctype": "DTR Device Log",
                        "employee": result[0]['user_id'],
                        "raw_data": json.dumps({**data, **result[0]}),
                        "log_date": data['date'],
                        "device_name": data['device_id']
                    }

                    frappe_client = utils.connect_erpnext(utils.config_server[result[0]['company']]['url'],
                                                          utils.config_server[result[0]['company']]['username'],
                                                          utils.config_server[result[0]['company']]['password'])

                    print(data)
                    utils.save_attendance(data, frappe_client)
                    os.remove(log)
                else:
                    print("employee not found rfid: " + data['rfid_number'])
            except:
                None


if __name__ == '__main__':
    upload_data()
