import random
from datetime import timedelta

import requests
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.timezone import now

from movies.models import Movie


USER_DATA = [
    {'user': {'username': 'john', 'first_name': 'John', 'last_name': 'Mayer', 'password': 'johnm123'},
     'movies': ['Rambo', 'Rocky']},
    {'user': {'username': 'nickb', 'first_name': 'Nickolas', 'last_name': 'Brody', 'password': 'ihavebeeninsyria123'},
     'movies': ['Lord of the rings', 'Harry Potter']},
    {'user': {'username': 'rogerf', 'first_name': 'Roger', 'last_name': 'Federer', 'password': 'iamthegoat123'},
     'movies': ['Amelie', 'Hunger Games']},
    {'user': {'username': 'alant', 'first_name': 'Alan', 'last_name': 'Turing', 'password': 'alanfort123'},
     'movies': ['Fast and Furious', 'Imitation game']},
    {'user': {'username': 'vanessam', 'first_name': 'Vanessa', 'last_name': 'May', 'password': 'vviolin123'},
     'movies': ['Jurassic Park', 'Titanic']},
]


class Command(BaseCommand):
    API_KEY = '4ef1db82'
    APP_ID = 'tt3896198'

    help = """ Create some user and import some movies using the OMDb api."""

    def create_movies(self, movie_title, user):
        query = 'http://www.omdbapi.com/?apikey=%(api_key)s&type=movie&s=%(query)s' % {
            'app_id': self.APP_ID, 'api_key': self.API_KEY, 'query': movie_title
        }
        response = requests.get(query)

        m_count = 0
        if response.status_code == 200:
            movies = response.json()['Search']

            for m in movies:
                movie_resp = requests.get(
                    'http://www.omdbapi.com/?apikey=%(api_key)s&type=movie&i=%(imdbID)s&plot=full' %
                    {'app_id': self.APP_ID, 'api_key': self.API_KEY, 'imdbID': m['imdbID']}
                )

                if movie_resp.status_code == 200:
                    movie = movie_resp.json()

                    try:
                        metascore = int(movie['Metascore'])
                    except ValueError:
                        metascore = 76

                    plot = movie['Plot']
                    if not plot or plot == 'N/A':
                        plot = """ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus dictum tellus 
                        massa, in molestie quam scelerisque ut. Mauris cursus, est et rutrum accumsan, diam est 
                        ultricies nulla, ac facilisis velit augue non ante. Sed orci sapien, scelerisque at orci eu, 
                        tincidunt rhoncus nisi. Phasellus ac nisi nisi. Duis sapien risus, posuere et dignissim in, 
                        blandit tristique lectus. Praesent blandit libero ut nisi aliquam efficitur. Vivamus et 
                        accumsan enim. Pellentesque sem nunc, tincidunt nec elit sit amet, ultricies fermentum dolor. 
                        Nulla nec egestas velit. Vivamus quis arcu quis elit dictum suscipit. Nulla ullamcorper rhoncus
                        malesuada. 
                         
                        Quisque et fringilla lacus, non congue quam. Ut eget lacus nec dolor sollicitudin scelerisque. 
                        Nam maximus elit eu tortor maximus, nec convallis lectus aliquam. Suspendisse potenti. Quisque 
                        mollis arcu non erat molestie, et pellentesque nunc pharetra. Aliquam posuere magna in commodo 
                        tincidunt. Integer mollis euismod libero, a mollis ipsum rutrum et. In ac pulvinar tortor, 
                        non."""

                    m_instance, created = Movie.objects.get_or_create(
                        title=movie['Title'],
                        description=plot,
                        likes=metascore,
                        hates=100 - metascore,
                        user=user
                    )
                    if created:
                        m_count += 1

                    m_instance.created_at = now() - timedelta(days=random.randint(10, 1000))
                    m_instance.save()

        return m_count

    def handle(self, *args, **options):
        movies_count = 0
        for ud in USER_DATA:
            user = User.objects.get_or_create(**ud['user'])

            self.stdout.write(self.style.WARNING('Importing some movies for user: %s' % user[0]))

            for m in ud['movies']:
                movies_count += self.create_movies(m, user=user[0])

        self.stdout.write(self.style.SUCCESS('Created 4 users and imported %s movies.' % movies_count))
