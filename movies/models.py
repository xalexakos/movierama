from django.contrib.auth.models import User
from django.db import models

from .settings import USER_VOTE_CHOICES, USER_VOTE_MAX_LENGTH


class Movie(models.Model):
    """ Movies model representation. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    hates = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserVote(models.Model):
    """ Mark whether a user has voted for a specific film. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote = models.CharField(choices=USER_VOTE_CHOICES, max_length=USER_VOTE_MAX_LENGTH)
