from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from movies.models import Movie, Like, Hate


class MovieModelTestCase(TestCase):
    def test_votes(self):
        """ Validates the automated created_at value. """
        user = User.objects.create(username='user', password='test')
        movie = Movie.objects.create(title='New Movie', description='A cool movie to watch.', user_id=user.pk)

        self.assertEqual(movie.created_at.date(), now().date())
        self.assertFalse(hasattr(movie, 'likes'))
        self.assertFalse(hasattr(movie, 'hates'))

        Like.objects.create(movie=movie)
        Hate.objects.create(movie=movie)

        self.assertEqual(movie.total_likes, 0)
        self.assertEqual(movie.total_hates, 0)

        # user likes the movie.
        with self.assertNumQueries(1):
            movie.likes.users.add(user)

        self.assertEqual(movie.total_likes, 1)
        self.assertEqual(movie.total_hates, 0)

        # user hates the movie.
        with self.assertNumQueries(2):
            movie.likes.users.remove(user)
            movie.hates.users.add(user)

        self.assertEqual(movie.total_hates, 1)
        self.assertEqual(movie.total_likes, 0)
