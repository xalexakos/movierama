from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.timezone import now

from .settings import USER_VOTE_CHOICES, USER_VOTE_MAX_LENGTH


class Movie(models.Model):
    """ Movies model representation. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    hates = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.title

    def get_created_repr(self):
        days_diff = (now().date() - self.created_at).days
        if not days_diff:
            return 'today'

        return '%s days ago' % days_diff


class UserVote(models.Model):
    """ Mark whether a user has voted for a specific film. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote = models.CharField(choices=USER_VOTE_CHOICES, max_length=USER_VOTE_MAX_LENGTH)

    class Meta:
        unique_together = ('user', 'movie')

    def save(self, *args, **kwargs):
        """ Increment movies likes or hates according to the user's vote value. """
        movie_column = self.vote + 's'
        setattr(self.movie, movie_column, F(movie_column) + 1)
        self.movie.save()

        super(UserVote, self).save(*args, **kwargs)
