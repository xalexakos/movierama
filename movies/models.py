from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from .settings import USER_VOTE_CHOICES, USER_VOTE_MAX_LENGTH


class Movie(models.Model):
    """ Movies model representation. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    hates = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.title

    def get_created_repr(self):
        date_diff = now() - self.created_at

        if not date_diff.days:
            hours_diff = int(date_diff.total_seconds() // 3600)

            if not hours_diff:
                return '%s minutes ago' % int(date_diff.total_seconds() // 60)

            return '%s hours ago' % int(date_diff.total_seconds() // 3600)

        return '%s days ago' % date_diff.days


class UserVote(models.Model):
    """ Mark whether a user has voted for a specific film. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote = models.CharField(choices=USER_VOTE_CHOICES, max_length=USER_VOTE_MAX_LENGTH)

    class Meta:
        unique_together = ('user', 'movie')
