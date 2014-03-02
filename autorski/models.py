from django.db import models


class Joke(models.Model):
    author = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    body = models.TextField()