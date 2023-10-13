# from tinydb import TinyDB, Query
# import utils
# import os
#
# Employee = Query()
# db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
# employees = db.all()
# for employee in employees:
#     if employee['rfid_number']:
#         if '209-192-105' in employee['rfid_number']:
#             print(employee)
#             break
#

import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

print(find('EMP00001*', 'images/'))