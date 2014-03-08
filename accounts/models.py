from django.db import models
from django.contrib.auth.models import User


class FacebookUser(models.Model):
    uid = models.CharField(max_length=120)
    access_token = models.CharField(max_length=300)
    expires = models.DateTimeField()
    username = models.CharField(max_length=120)
    user = models.OneToOneField(User, related_name='facebook', blank=True, null=True)