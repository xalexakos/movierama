from django.views.generic import ListView

from .models import Movie


class MovieListPageView(ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'movies'
    paginate_by = 2

    ordering = ['-likes', 'title']

    def get_ordering(self):
        return self.request.GET.get('ordering') or self.ordering

    def get_queryset(self):
        queryset = super(MovieListPageView, self).get_queryset()

        user_filter = self.request.GET.get('user')
        if user_filter:
            queryset = queryset.filter(user_id=user_filter)

        return queryset
