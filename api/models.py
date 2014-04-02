import json

from django.db import models
import requests

from Suchary.settings import GCM_API_KEY


class Device(models.Model):
    registration_id = models.TextField()
    active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def send_data(self, data):
        url = 'https://android.googleapis.com/gcm/send'
        header = {'Authorization': 'key=' + GCM_API_KEY, 'Content-Type': 'application/json'}
        payload = {'registration_ids': [self.registration_id], 'data': data}
        r = requests.post(url, data=json.dumps(payload), headers=header)
        return r

    def __str__(self):
        return str(self.registration_id)