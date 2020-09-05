from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from movies.models import Movie


class MovieUniqueTitleValidator(TestCase):
    def test_title_validation(self):
        """ Validate unique title. """
        user = User.objects.create(username='user', password='test')
        Movie.objects.create(title='New Movie', description='A cool movie to watch.', user_id=user.pk)

        m = Movie(title='new Movie', description='A cool movie to watch.', user_id=user.pk)
        self.assertRaisesMessage(ValidationError, 'A movie with this title already exists.', m.full_clean)
