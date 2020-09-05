from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from movies.models import Movie, UserVote
from movies.settings import USER_VOTE_LIKE


class MovieModelTestCase(TestCase):
    def test_defaults(self):
        """ Validates the automated created_at value. """
        user = User.objects.create(username='user', password='test')
        m = Movie.objects.create(title='New Movie', description='A cool movie to watch.', user_id=user.pk)
        self.assertEqual(m.likes, 0)
        self.assertEqual(m.hates, 0)
        self.assertEqual(m.created_at, now().date())


class UserVoteModelTestCase(TestCase):
    def test_create(self):
        """ Validates the automated increment of likes and hates values. """
        user = User.objects.create(username='user', password='test')
        movie = Movie.objects.create(title='New Movie', description='A cool movie to watch.',
                                     user_id=user.pk, likes=10, hates=2)

        with self.assertNumQueries(1):
            UserVote.objects.create(user_id=user.pk, movie_id=movie.pk, vote=USER_VOTE_LIKE)

        # validate tha the user cannot vote again for the same movie.
        self.assertRaises(IntegrityError, UserVote.objects.create, user_id=user.pk, movie_id=movie.pk,
                          vote=USER_VOTE_LIKE)
