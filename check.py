from frappeclient import FrappeClient
import ConfigParser
import os
import json
import subprocess
import uuid


path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(path + '/rfid.ini')

server_url = config.get('tailerp', 'url')
server_username = config.get('tailerp', 'username')
server_password = config.get('tailerp', 'password')


def ping(site):
    client = FrappeClient(server_url, server_username, server_password)
    data = {}

    if os.path.isfile('/tmp/tmate.dat'):
        try:
            result = subprocess.check_output(['cat', '/tmp/tmate.dat'])
        except subprocess.CalledProcessError as exc:
            result = exc.output

        data['device_id'] = str(hex(uuid.getnode()))
        data['site'] = site
        data['connection_string'] = result

        params = {"message": json.dumps(data)}

        try:
            client.post_api("wela_erpnext.rests.ping", params)
        except:
            None

ping(server_url)

