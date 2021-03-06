from django.db import models


class Joke(models.Model):
    site = models.CharField(max_length=100)
    key = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    votes = models.IntegerField()
    date = models.DateTimeField()
    url = models.URLField()
    body = models.TextField()
    duplicate = models.ForeignKey('self', blank=True, null=True)
    added = models.DateTimeField()
    hidden = models.DateTimeField(blank=True, null=True, default=None)
    verified = models.DateTimeField(blank=True, null=True, default=None)
    changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.key)
