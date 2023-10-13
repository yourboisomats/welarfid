from frappeclient import FrappeClient
client = FrappeClient('https://khs.wela.online', 'device@wela.online', 'qwerty')

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
device_serial = get_serial()
param = {"serial": device_serial}
# /home/jvfiel/frappe-bench/apps/wela/wela/tasks/sync_attendance.py
students = client.get_api("wela.tasks.sync_attendance.getSyncSelectedStudent", param)
#print students
for student in students:
    print student