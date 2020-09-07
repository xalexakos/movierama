from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from .validators import unique_movie_title


class Movie(models.Model):
    """ Movies model representation. """
    title = models.CharField(max_length=255, validators=[unique_movie_title])
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.title

    def save(self, *args, **kwargs):
        """
        Intervene to the users title format.
        Each word should be saved with the first letter in uppercase and the rest in lowercase.
        """
        self.title = u' '.join([word.capitalize() for word in self.title.split()])

        super(Movie, self).save(*args, **kwargs)

    @property
    def total_likes(self):
        if hasattr(self, 'likes'):
            return self.likes.users.count()

        return 0

    @property
    def total_hates(self):
        if hasattr(self, 'hates'):
            return self.hates.users.count()

        return 0

    def get_created_repr(self):
        """ Formats the date to the closest interval (seconds, minutes, hours, days, months, years). """
        date_diff = now() - self.created_at

        if not date_diff.days:
            hours_diff = int(date_diff.total_seconds() // 3600)

            if not hours_diff:
                return '%s minutes ago' % int(date_diff.total_seconds() // 60)

            return '%s hours ago' % int(date_diff.total_seconds() // 3600)

        else:
            if date_diff.days // 365:
                return '%s years ago' % int(date_diff.days // 365)
            elif date_diff.days // 30:
                return '%s months ago' % int(date_diff.days // 30)
            else:
                return '%s days ago' % int(date_diff.days)


# User votes can be represented in two models, one for likes and one for hates.
# Going that way will make it easier to handle like/hate vote counts when a user either updates his vote or
# entirely removes it.
# create, update timestamps are handle automatically during create/update operations.
class Like(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='likes')
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Hate(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='hates')
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
