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


def send(data, collapse_key=None, to=None, reg_ids=None):
    if reg_ids is None:
        reg_ids = get_reg_ids(to)

    if len(reg_ids) > 1000:
        logger.info('reg ids too long ({}). '.format(len(reg_ids)))
        send(data, collapse_key, to, reg_ids[:1000])
        send(data, collapse_key, to, reg_ids[1000:])
        return

    payload = {'registration_ids': reg_ids, 'data': data}
    if collapse_key is not None:
        payload.update({'collapse_key': collapse_key})
    logger.debug('Sending GCM data:\n%s\nto %d devices with collapse key %s', data, len(reg_ids), collapse_key)
    r = requests.post(URL, data=json.dumps(payload), headers=HEADER)
    handle_gcm_response(r, reg_ids)


def edit_joke(key):
    data = {
        'type': 'edit',
        'key': key
    }
    send_change()
    send(data)


def new_jokes():
    data = {
        'type': 'new'
    }
    send_change()
    send(data, 'new')


def delete_joke(key):
    data = {
        'type': 'delete',
        'key': key
    }
    send_change()
    send(data)


def send_change():
    data = {
        'type': 'change'
    }
    send(data, 'change')


def send_message(title, body, alias=None):
    data = {
        'type': 'message',
        'title': title,
        'text': body
    }
    send(data, to=alias)


def handle_gcm_response(r, reg_ids):
    if r.status_code != 200:
        logger.error('GCM send code %d\n%s', r.status_code, r.text)
        return
    logger.debug('GCM response:\n%s', r.text)
    response = r.json()
    if response['failure']:
        for i, result in enumerate(response['results']):
            if 'error' in result and result['error'] == 'NotRegistered':
                reg_id = reg_ids[i]
                device = Device.objects.get(registration_id=reg_id)
                device.active = False
                device.save()
                logger.warning('Device %s is not registered', device.pk)