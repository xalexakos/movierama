from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import MovieCreateForm
from .models import Movie


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
        queryset = super(MovieListPageView, self).get_queryset() \
            .prefetch_related('user', 'likes__users', 'hates__users')

        user_filter = self.request.GET.get('user')
        if user_filter:
            queryset = queryset.filter(user_id=user_filter)

        return queryset


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
