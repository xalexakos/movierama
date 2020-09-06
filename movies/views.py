from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .forms import MovieCreateForm
from .models import Movie, Like, Hate
from .utils import get_response_query_params


class MovieListPageView(ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'movies'
    paginate_by = 10

    ordering = ['-likes', 'title']

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering and hasattr(self.model, ordering.replace('-', '')):
            return ordering

        return super(MovieListPageView, self).get_ordering()

    def get_queryset(self):
        """ Create a custom method to handle m2m relationship ordering and user filtering. """
        queryset = self.model.objects.prefetch_related('user', 'likes__users', 'hates__users')

        user_filter = self.request.GET.get('u')
        if user_filter:
            queryset = queryset.filter(user_id=user_filter)

        ordering = self.get_ordering()
        if ordering:

            if 'likes' in ordering or 'hates' in ordering:
                vote_ordering = ordering.replace('-', '')
                queryset = queryset.annotate(**{'%s_count' % vote_ordering: Count('%s__users' % vote_ordering)})
                ordering = '%s_count' % ordering

            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MovieListPageView, self).get_context_data(*args, **kwargs)

        user_id = self.request.GET.get('u')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            context['user_filter'] = '%s %s' % (user.first_name, user.last_name)

        ordering = self.request.GET.get('ordering', None)
        context['active_ordering'] = ordering is not None

        return context


class MovieAddPageView(ListView):
    model = Movie
    template_name = 'movies/add_movie.html'
    context_object_name = 'movies'

    def get_context_data(self, *args, **kwargs):
        context = super(MovieAddPageView, self).get_context_data(*args, **kwargs)
        context['form'] = MovieCreateForm()

        return context

    def get_post_value(self, value):
        """ """
        post_value = self.request.POST.get(value)
        if post_value:
            post_value = post_value

        # strip all whitespaces.
        return post_value.lstrip().rstrip() if post_value else post_value

    def post(self, request, *args, **kwargs):
        post_data = {
            'user': self.request.user,
            'title': self.get_post_value('title'),
            'description': self.get_post_value('description')
        }

        form = MovieCreateForm(data=post_data)
        if form.is_valid():
            form.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})


class MovieVoteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """ Let user vote for a movie that he did not register. """
        movies = Movie.objects.exclude(user_id=self.request.user.id)
        movie = get_object_or_404(movies, pk=self.kwargs.get('movie_id'))

        # initialize the movie -> vote relations in case they do not already exists
        # (this should be executed when a movie is being voted for the first time.)
        if not hasattr(movie, 'likes'):
            Like.objects.create(movie=movie)

        if not hasattr(movie, 'hates'):
            Hate.objects.create(movie=movie)

        # when a user is voting:
        # check if this vote already exists.
        # in case it does remove the vote.
        # in case it does not add a new vote and remove any possible counter vote.
        vote = self.kwargs.get('vote')
        if vote.lower() == 'like':
            if request.user in movie.likes.users.all():
                movie.likes.users.remove(request.user)
            else:
                movie.likes.users.add(request.user)
                movie.hates.users.remove(request.user)
        elif vote.lower() == 'hate':
            if request.user in movie.hates.users.all():
                movie.hates.users.remove(request.user)
            else:
                movie.hates.users.add(request.user)
                movie.likes.users.remove(request.user)

        return redirect(reverse('movies_list_view') + get_response_query_params(self.request))
