from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from movies.models import Movie, Like, Hate


class MovieListPageViewTestCase(TestCase):
    view_name = 'movies_list_view'

    def setUp(self) -> None:
        super(MovieListPageViewTestCase, self).setUp()

        self.user = User.objects.create(username='test_user', password='test_password')

        self.m1 = Movie.objects.create(title='A movie', description='A nice movie.', user=self.user)
        Like.objects.create(movie=self.m1)
        self.m1.likes.users.add(self.user)

        self.m2 = Movie.objects.create(title='B movie', description='Another nice movie.', user=self.user)
        Hate.objects.create(movie=self.m2)
        self.m2.hates.users.add(self.user)

        self.m1.created_at = (now() - timedelta(days=1))
        self.m1.save()
        self.m2.created_at = (now() - timedelta(days=2))
        self.m2.save()

    def test_default_ordering(self):
        """ MovieListPageView get() method with default ordering. """
        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name))

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

    def test_likes_ordering(self):
        """ MovieListPageView get() method ordered by likes. """
        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=likes')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m2, self.m1])

        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=-likes')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

    def test_hates_ordering(self):
        """ MovieListPageView get() method ordered by hates. """
        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=hates')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=-hates')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m2, self.m1])

    def test_created_ordering(self):
        """ MovieListPageView get() method ordered by hates. """
        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=created_at')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m2, self.m1])

        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=-created_at')

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])

    def test_invalid_ordering(self):
        """ MovieListPageView get() method ordered by hates. """
        with self.assertNumQueries(7):
            response = self.client.get(reverse(self.view_name) + '?ordering=a')

        self.assertEqual(response.status_code, 200)
        # the default ordering is preserved.
        self.assertListEqual(list(response.context['movies']), [self.m1, self.m2])


class MovieAddPageViewTestCase(TestCase):
    view_name = 'movies_add_view'

    def setUp(self) -> None:
        super(MovieAddPageViewTestCase, self).setUp()

        self.user = User.objects.create(username='test_user', password='test_password')

    def test_get(self):
        """ MovieAddPageView get() method. """
        with self.assertNumQueries(0):
            response = self.client.get(reverse(self.view_name), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/user/login/?next=/add-movie/')

        self.client.force_login(self.user)
        with self.assertNumQueries(2):
            response = self.client.get(reverse(self.view_name), follow=True)

        self.assertEqual(response.status_code, 200)

        response_form = response.context['form']
        self.assertCountEqual([f for f in response_form.fields], ['title', 'description', 'user'])

    def test_post_unauthenticated_user(self):
        """ MovieAddPageView get() method with unauthenticated user. """
        with self.assertNumQueries(0):
            response = self.client.post(reverse(self.view_name), {},  follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/user/login/?next=/add-movie/')

    def test_post_validations(self):
        """ MovieAddPageView get() method post data validations. """
        self.client.force_login(self.user)
        with self.assertNumQueries(4):
            response = self.client.post(reverse(self.view_name), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['title'].errors, ['This field is required.'])
        self.assertEqual(response.context['form']['description'].errors, ['This field is required.'])

        self.assertEqual(Movie.objects.count(), 0)

        # empty values
        with self.assertNumQueries(4):
            response = self.client.post(reverse(self.view_name), {'title': '', 'description': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['title'].errors, ['This field is required.'])
        self.assertEqual(response.context['form']['description'].errors, ['This field is required.'])

        self.assertEqual(Movie.objects.count(), 0)

        # existing movie.
        Movie.objects.create(title='A movie', description='A nice movie.', user=self.user)
        with self.assertNumQueries(5):
            response = self.client.post(reverse(self.view_name), {'title': 'A movie', 'description': 'Desc'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['title'].errors, ['A movie with this title already exists.'])

        self.assertEqual(Movie.objects.count(), 1)

    def test_post_add_movie(self):
        """ MovieAddPageView get() method create a new movie. """
        self.client.force_login(self.user)
        with self.assertNumQueries(13):
            response = self.client.post(reverse(self.view_name), {'title': 'A movie', 'description': 'Desc'},
                                        follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.filter(title='A Movie').count(), 1)


class MovieVoteViewTestCase(TestCase):
    view_name = 'movies_vote_view'

    def setUp(self) -> None:
        super(MovieVoteViewTestCase, self).setUp()

        self.user = User.objects.create(username='test_user', password='test_password')

    def test_unauthorized_user(self):
        """ MovieVoteView get() with a non authorized user. """
        movie = Movie.objects.create(title='Batman Begins', description='Movie of a lifetime0', user=self.user)

        with self.assertNumQueries(0):
            response = self.client.get(reverse(self.view_name, args=[movie.id, 'like']), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/user/login/?next=/vote/%s/like/' % movie.id)

    def test_movie_owner(self):
        """ MovieVoteView get() with an owner's vote. """
        self.client.force_login(self.user)
        movie = Movie.objects.create(title='Batman Begins', description='Movie of a lifetime0', user=self.user)

        with self.assertNumQueries(3):
            response = self.client.get(reverse(self.view_name, args=[movie.id, 'like']), follow=True)

        self.assertEqual(response.status_code, 404)

    def test_vote(self):
        """ MovieVoteView get() with a valid vote. """
        self.client.force_login(self.user)

        user = User.objects.create(username='batman', password='begins')
        movie = Movie.objects.create(title='Batman Begins', description='Movie of a lifetime0', user=user)

        with self.assertNumQueries(21):
            response = self.client.get(reverse(self.view_name, args=[movie.id, 'like']), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

        movie.refresh_from_db()
        self.assertEqual(movie.total_likes, 1)
        self.assertEqual(movie.total_hates, 0)

    def test_remove_vote(self):
        """ MovieVoteView get() retrieve a valid vote. """
        self.client.force_login(self.user)

        user = User.objects.create(username='batman', password='begins')
        movie = Movie.objects.create(title='Batman Begins', description='Movie of a lifetime0', user=user)
        Like.objects.create(movie=movie)
        movie.likes.users.add(self.user)

        self.assertEqual(movie.total_likes, 1)
        self.assertEqual(movie.total_hates, 0)

        with self.assertNumQueries(19):
            response = self.client.get(reverse(self.view_name, args=[movie.id, 'like']), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

        movie.refresh_from_db()
        self.assertEqual(movie.total_likes, 0)
        self.assertEqual(movie.total_hates, 0)

    def test_update_vote(self):
        """ MovieVoteView get() update a valid vote. """
        self.client.force_login(self.user)

        user = User.objects.create(username='batman', password='begins')
        movie = Movie.objects.create(title='Batman Begins', description='Movie of a lifetime0', user=user)
        Like.objects.create(movie=movie)
        movie.likes.users.add(self.user)

        self.assertEqual(movie.total_likes, 1)
        self.assertEqual(movie.total_hates, 0)

        with self.assertNumQueries(20):
            response = self.client.get(reverse(self.view_name, args=[movie.id, 'hate']), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

        movie.refresh_from_db()
        self.assertEqual(movie.total_likes, 0)
        self.assertEqual(movie.total_hates, 1)
