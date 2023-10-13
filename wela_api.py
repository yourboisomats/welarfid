from rfid_utils import get_serial

from db import *
from frappeclient import FrappeClient
import shutil
import os
from sqlalchemy import asc
import time
import memcache
import json
import sys

client = FrappeClient(url, username, password)

#/home/jvfiel/frappe-wela-v7/apps/wela/wela/attendance/report/students_no_dtr_log/students_no_dtr_log.py
def sync_student_modified():
    device_serial = get_serial()
    param = {"serial": device_serial}
    students = client.get_api("wela.rest.student_list", param)
    data = session()
    if students:
        print len(students)

    print students

    return students


def sync_student(sync_pictures="True"):
    device_serial = get_serial()
    param = {"serial": device_serial}
    #/home/jvfiel/frappe-bench/apps/wela/wela/tasks/sync_attendance.py
    students = client.get_api("wela.tasks.sync_attendance.getSyncSelectedStudent", param)
    data = session()
    # print students
    if students:
        print len(students)
    return students
#TEST 1
# sync_student()
sync_student_modified()