import json

from django.db import models
import requests

from Suchary.settings import GCM_API_KEY


class Device(models.Model):
    registration_id = models.TextField()
    android_id = models.TextField(unique=True)
    alias = models.TextField(blank=True)
    version = models.CharField(max_length=20)
    model = models.CharField(max_length=60)
    os_version = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
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
        if self.alias:
            return str(self.alias)
        return str(self.registration_id)