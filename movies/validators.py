from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django.utils.translation import ugettext


def unique_movie_title(title):
    from movies.models import Movie
    if Movie.objects.annotate(title__lower=Lower('title')).filter(title__lower=title.lower().strip()).exists():
        raise ValidationError(ugettext('A movie with this title already exists.'))
