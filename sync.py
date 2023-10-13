from db import *
from frappeclient import FrappeClient
import shutil
import os
from sqlalchemy import asc
import time
import memcache
import json

client = FrappeClient(url, username, password)


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


def sync_dtr():
    data = session()
    dtrs = data.query(DTR).filter(DTR.synced == 0).order_by(asc(DTR.time_login)).all()
    for dtr in dtrs:
        try:
            params = {"id_number": dtr.id_number, "date_login": dtr.time_login,
                      "device_serial": get_serial(), "kind": dtr.kind
                      }
            # print params
            try:
                ret = client.post_api("wela.rest.dtr", params)
                if ret['status'] == 'ok':
                    dtr.synced = 1
                    data.commit()
                else:
                    print ret
            except Exception,e:
                print "inner catch error {0}".format(e)
        except Exception,e:
            print "outer catch error {1}".format(e)

def sync_student():
    device_serial = get_serial()
    param = {"serial": device_serial}
    students = client.get_api("wela.rest.student_list", param)
    data = session()
    if students:
        for student in students:
            if student["id_number"]:
                id_ = student["school_year"] + '-' + student["id_number"]
                image_file = ''

                if student["id_picture"]:
                    filename, file_extension = os.path.splitext(student["id_picture"])
                    image_file = image_path + '/' + id_ + file_extension

                found = data.query(Student).filter(Student.id == id_).all()
                if len(found) == 0:
                    found = None
                else:
                    found = found[0]
                if not found:
                    new = Student(first_name=student["first_name"], middle_name=student["middle_name"],
                                  school_year=student["school_year"], last_name=student["last_name"],
                                  section=student["section"], level=student["level"], id_number=student["id_number"],
                                  rfid=student["rfid"], id_picture=image_file, id=id_, kind=student["kind"],
                                  chinese_name=student["chinese_name"], lunch_pass=student["lunch_pass"], commuter_pass=student["commuter_pass"]
                                  )
                    data.add(new)
                else:
                    found.first_name = student["first_name"]
                    found.middle_name = student["middle_name"]
                    found.last_name = student["last_name"]
                    found.section = student["section"]
                    found.level = student["level"]
                    found.rfid = student["rfid"]
                    found.kind = student["kind"]
                    found.chinese_name = student["chinese_name"]
                    found.lunch_pass = student["lunch_pass"]
                    found.commuter_pass = student["commuter_pass"]
                    found.id_picture = image_file

                if student["id_picture"]:
                    try:
                        r = client.session.get(url + str(student["id_picture"]), stream=True)
                        if r.status_code == 200:
                            with open(image_file, 'wb') as f:
                                r.raw.decode_content = True
                                shutil.copyfileobj(r.raw, f)
                    except:
                        None
                data.commit()


def ping():
    device_serial = get_serial()
    param = {"serial": device_serial}
    return client.get_api("wela.rest.ping", param)


if __name__ == '__main__':
    count_student = 30
    while True:
        if count_student >= 30:
            shared = memcache.Client(['127.0.0.1:11211'], debug=0)
            try:
                sync_student()
                res = ping()
                count_student = 0
                if school_year != res["school_year"] or school_name != res["school_name"] or time_diff != res["time_diff"] or kind != res["kind"]:
                    Config.set('data', 'school_year', res["school_year"])
                    Config.set('data', 'school_name', res["school_name"])
                    Config.set('data', 'time_diff', str(res["time_diff"]))
                    Config.set('data', 'kind', str(res["kind"]))
                    school_name = res["school_name"]
                    school_year = res["school_year"]
                    time_diff = res["time_diff"]
                    kind = res["kind"]

                    f = open("{0}/rfid.ini".format(os.path.dirname(os.path.abspath(__file__))), 'w')
                    Config.write(f)
                    f.close()

                json_data = {'status': "ONLINE", 'school_year': res["school_year"],
                             'school_name': res["school_name"], 'time_diff': res["time_diff"], 'kind': res['kind']
                             }
            except:
                json_data = {'status': "OFFLINE", 'school_year': school_year,
                             'school_name': school_name, 'time_diff': time_diff, 'kind': kind
                             }
        shared.set('connection', json.dumps(json_data))
        count_student += 1
        try:
            sync_dtr()
        except:
            None
        time.sleep(5)
