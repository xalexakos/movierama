from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from movies.models import Movie


class MovieListPageViewTestCase(TestCase):
    view_url = ''

    def setUp(self) -> None:
        super(MovieListPageViewTestCase, self).setUp()

        self.user = User.objects.create(username='test_user', password='test_password')

        self.m1 = Movie.objects.create(title='A movie', description='A nice movie.', user=self.user,
                                       likes=15, hates=3)
        self.m2 = Movie.objects.create(title='B movie', description='Another nice movie.', user=self.user,
                                       likes=12, hates=6)

        self.m1.created_at = (now() - timedelta(days=1)).date()
        self.m1.save()
        self.m2.created_at = (now() - timedelta(days=2)).date()
        self.m2.save()

    def test_default_ordering(self):
        """ MovieListPageView get() method with default ordering. """
        with self.assertNumQueries(3):
            response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

    def test_likes_ordering(self):
        """ MovieListPageView get() method ordered by likes. """
        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=likes')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m2, self.m1])

        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=-likes')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

    def test_hates_ordering(self):
        """ MovieListPageView get() method ordered by hates. """
        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=hates')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=-hates')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m2, self.m1])

    def test_created_ordering(self):
        """ MovieListPageView get() method ordered by hates. """
        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=created_at')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m2, self.m1])

        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=-created_at')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

    def test_invalid_ordering(self):
        """ MovieListPageView get() method ordered by hates. """
        with self.assertNumQueries(3):
            response = self.client.get(self.view_url + '?ordering=a')

        self.assertEqual(response.status_code, 200)
        # the default ordering is preserved.
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])
