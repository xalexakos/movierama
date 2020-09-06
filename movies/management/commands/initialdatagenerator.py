import random
from datetime import timedelta

import requests
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils.timezone import now

from movies.models import Movie, Like, Hate

USER_DATA = [
    {'user': {'username': 'jonny', 'first_name': 'Jonny', 'last_name': 'Greenwood', 'password': 'jonnygw123'},
     'movies': ['The Shawshank Redemption', 'The Godfather', 'The Godfather: Part II']},
    {'user': {'username': 'rogerf', 'first_name': 'Roger', 'last_name': 'Federer', 'password': 'iamthegoat123'},
     'movies': ['The Dark Knight', '12 Angry Men', 'Schindler\'s List', 'Inception']},
    {'user': {'username': 'maisie', 'first_name': 'Maisie', 'last_name': 'Williams', 'password': 'aryastark123'},
     'movies': ['The Lord of the Rings: The Return of the King', 'Pulp Fiction', 'Forrest Gump']},
    {'user': {'username': 'vanessam', 'first_name': 'Vanessa', 'last_name': 'May', 'password': 'vviolin123'},
     'movies': ['The Good, the Bad and the Ugly', 'The Lord of the Rings: The Fellowship of the Ring', 'Fight Club']},
]


class Command(BaseCommand):
    API_KEY = '4ef1db82'
    APP_ID = 'tt3896198'

    help = """ Create some user and import some movies using the OMDb api."""

    def create_movies(self, movies, user):
        self.stdout.write(self.style.ERROR('Importing some movies for user: %s' % user))

        movies_added = []
        for m in movies:
            movie_resp = requests.get(
                'http://www.omdbapi.com/?apikey=%(api_key)s&type=movie&t=%(title)s&plot=full' %
                {'app_id': self.APP_ID, 'api_key': self.API_KEY, 'title': m}
            )

            if movie_resp.status_code == 200:
                movie = movie_resp.json()

                m_instance, created = Movie.objects.get_or_create(
                    title=movie['Title'],
                    description=movie['Plot'],
                    user=user
                )

                if created:
                    movies_added.append(m_instance.id)

                    self.stdout.write(self.style.WARNING('Added "%s" movie' % movie['Title']))

                # randomize the added dates.
                m_instance.created_at = now() - timedelta(days=random.randint(10, 1000))
                m_instance.save()

                Like.objects.get_or_create(movie=m_instance)
                Hate.objects.get_or_create(movie=m_instance)

        return movies_added

    def handle(self, *args, **options):
        for ud in USER_DATA:
            user = User.objects.get_or_create(**ud['user'])
            self.create_movies(ud['movies'], user=user[0])

        # create some extra users just to vote.
        for i in range(20):
            try:
                User.objects.create(
                    username='username' + str(i + 1),
                    password='userpassword' + str(i + 1),
                    first_name='User' + str(i + 1),
                    last_name='User' + str(i + 1),
                )
            except IntegrityError:
                pass

        self.stdout.write(self.style.WARNING('Now its time to vote.'))
        for u in User.objects.all():
            for movie in Movie.objects.exclude(user=u):

                dice_1000 = random.randint(1, 1000)
                if dice_1000 < 700 and u not in movie.likes.users.all():
                    movie.likes.users.add(u)
                elif u not in movie.hates.users.all():
                    movie.hates.users.add(u)

        self.stdout.write(self.style.SUCCESS('All votes were successfully submitted.'))
