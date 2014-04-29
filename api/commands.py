import json
import requests
from Suchary.local_settings import GCM_API_KEY
from api.models import Device

URL = 'https://android.googleapis.com/gcm/send'
HEADER = {'Authorization': 'key=' + GCM_API_KEY, 'Content-Type': 'application/json'}


def get_reg_ids():
    reg_ids = [device.registration_id for device in Device.objects.filter(active=True)]
    return reg_ids


def send(data, collapse_key=None):
    reg_ids = get_reg_ids()
    payload = {'registration_ids': reg_ids, 'data': data}
    if collapse_key is not None:
        payload.update({'collapse_key': collapse_key})
    r = requests.post(URL, data=json.dumps(payload), headers=HEADER)


def edited_joke(key):
    data = {
        'type': 'edit',
        'key': key
    }
    send(data)


def new_jokes(count, last, keys):
    data = {
        'type': 'new',
        'count': count,
        'body': last,
        'keys': ' '.join(keys)
    }
    send(data)