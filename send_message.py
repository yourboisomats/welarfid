import subprocess
import utils
import glob
import json
from tinydb import TinyDB, Query
import os
import time
from rocketchat_API.rocketchat import RocketChat


def create_gammu_config():
    try:
        result = subprocess.check_output('gammu-detect', shell=True)
    except subprocess.CalledProcessError as exc:
        result = exc.output

    with open('gammu.cfg', 'wb') as f:
        print(result)
        f.write(result)


def send_gammu(mobile_number, message):
    try:
        res = subprocess.check_output('gammu -c ' + (
                utils.path + "/gammu.cfg") + ' sendsms TEXT ' + mobile_number + '  -text "' + message + '"',
                                      shell=True)
    except subprocess.CalledProcessError as exc:
        res = exc.output
    print(res)


def chat_message(text):
    try:
        rocket = RocketChat('inday', 'qwerty123456', server_url='https://chat.bai.ph')
        rocket.chat_post_message(text, channel='bai-wela')
    except:
        None


def check_log(type):
    Employee = Query()
    db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')

    for log in glob.glob(utils.path + "/data/*" + ".sms"):
        with open(log) as json_file:
            try:
                data = json.load(json_file)
            except:
                pass

            result = db.search(Employee.attendance_device_id == str(data['rfid_number']).strip())
            if len(result) > 0:
                if data['direction'] == "IN":
                    message = str(utils.config.get("sms", "message_in")).strip().format(time=data['date'],
                                                                                        name=result[0]['name'],
                                                                                        direction=data['direction'])
                else:
                    message = str(utils.config.get("sms", "message_out")).strip().format(time=data['date'],
                                                                                         name=result[0]['name'],
                                                                                         direction=data['direction'])
                if type == 'chat':
                    if str(data['direction']).strip() == 'TIME':
                        chat_message(message)
                else:
                    mobile_numbers = str(utils.config.get("sms", "mobile_numbers")).strip().split(",")
                    for mobile_number in mobile_numbers:
                        try:
                            send_gammu(mobile_number, message)
                        except:
                            None
            os.remove(log)
            time.sleep(10)


if __name__ == '__main__':
    check_log(str(utils.config.get("sms", "type")).strip())
