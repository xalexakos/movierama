from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from .models import Movie


class MovieModelTestCase(TestCase):
    def test_defaults(self):
        """ Validates the automated created_at value. """
        user = User.objects.create(username='user', password='test')
        m = Movie.objects.create(title='New Movie', description='A cool movie to watch.', user_id=user.pk)
        self.assertEqual(m.likes, 0)
        self.assertEqual(m.hates, 0)
        self.assertEqual(m.created_at, now().date())
