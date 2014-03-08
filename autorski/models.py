from django.db import models
from django.contrib.auth.models import User


class Joke(models.Model):
    author = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    upvotes = models.ManyToManyField(User, related_name='upvoted')
    downvotes = models.ManyToManyField(User, related_name='downvoted')

    @property
    def votes(self):
        return self.upvotes.count() - self.downvotes.count()