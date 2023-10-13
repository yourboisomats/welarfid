import memcache
import json
shared = memcache.Client(['127.0.0.1:11211'], debug=0)
json_student = {'status': 'VALID', 'kind': u'Teacher', 'name': u'Sheba Mae A Europa', 'level': None, 'id_number': u'00011', 'section': None, 'id_picture': u''}
shared.set('message', json.dumps(json_student))
