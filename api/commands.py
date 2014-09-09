import json
import logging

import requests

from Suchary.local_settings import GCM_API_KEY
from api.models import Device


URL = 'https://android.googleapis.com/gcm/send'
HEADER = {'Authorization': 'key=' + GCM_API_KEY, 'Content-Type': 'application/json'}

logger = logging.getLogger(__name__)


def get_reg_ids(alias):
    devices = Device.objects.filter(active=True)
    if alias:
        devices = devices.filter(alias=alias)
    reg_ids = [device.registration_id for device in devices]
    return reg_ids


def send(data, collapse_key=None, to=None):
    reg_ids = get_reg_ids(to)
    payload = {'registration_ids': reg_ids, 'data': data}
    if collapse_key is not None:
        payload.update({'collapse_key': collapse_key})
    logger.debug('Sending GCM data:\n%s\nto %d devices with collapse key %s', data, len(reg_ids), collapse_key)
    r = requests.post(URL, data=json.dumps(payload), headers=HEADER)
    logger.debug('GCM response:\n%s', r.text)


def edit_joke(key):
    data = {
        'type': 'edit',
        'key': key
    }
    send(data)


def new_jokes():
    data = {
        'type': 'new'
    }
    send(data, 'new')


def delete_joke(key):
    data = {
        'type': 'delete',
        'key': key
    }
    send(data)


def send_message(title, body, alias=None):
    data = {
        'type': 'message',
        'title': title,
        'text': body
    }
    send(data, to=alias)