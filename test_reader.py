import memcache
from sqlalchemy import and_
import json
import MFRC522
import signal
from time import sleep
from db import *
from pyA20.gpio import gpio
from pyA20.gpio import port

buzzer = port.PA20
light = port.PD14

gpio.init()
gpio.setcfg(buzzer, gpio.OUTPUT)
gpio.setcfg(light, gpio.OUTPUT)

continue_reading = True
MIFAREReader = MFRC522.MFRC522()


def end_read(signal, frame):
    global continue_reading
    continue_reading = False
    print "Ctrl+C captured, ending read."
    MIFAREReader.GPIO_CLEEN()


signal.signal(signal.SIGINT, end_read)

while continue_reading:
    # (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # if status == MIFAREReader.MI_OK:
    #     # print "Card detected"
    #     pass
    # (status, backData) = MIFAREReader.MFRC522_Anticoll()
    # if status == MIFAREReader.MI_OK:

    shared = memcache.Client(['127.0.0.1:11211'], debug=0)
    # rfid = str(backData[0]) + "-" + str(backData[1]) + "-" + str(backData[2]) + "-" + \
    #        str(backData[3]) + "-" + str(backData[4])
    data = session()

    import random

    rand = random.randrange(0, data.query(Student).count())

    found = data.query(Student).filter(Student.school_year == school_year)[rand]

    # print found

    # if found:
    #     found = None
    #     json_student = {'status': 'INVALID', 'id_number': ''}
    # else:
    student_data = found
    middle_name = ''
    if student_data.middle_name:
        middle_name = student_data.middle_name
    full_name = student_data.first_name + ' ' + middle_name + ' ' + student_data.last_name
    print full_name
    json_student = {'name': full_name, 'id_number': student_data.id_number, 'status': 'VALID',
                    'section': student_data.section, 'level': student_data.level, 'chinese_name': student_data.chinese_name,
                    'lunch_pass': student_data.lunch_pass, 'commuter_pass': student_data.commuter_pass,
                    'kind': student_data.kind, 'id_picture': student_data.id_picture}

    try:
        # new = DTR(time_login=get_time(), id_number=student_data.id_number, kind=student_data.kind)
        # data.add(new)
        # data.commit()
        gpio.output(buzzer, 1)
        gpio.output(light, 1)
        sleep(0.2)
        gpio.output(buzzer, 0)
        gpio.output(light, 0)
    except Exception,e:
        print e

    shared.set('message', json.dumps(json_student))

    sleep(1.0)

