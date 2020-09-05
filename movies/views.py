from django.views.generic import ListView

from .models import Movie


class MovieListPageView(ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'movies'
    paginate_by = 10

    ordering = ['-likes', 'title']

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering and hasattr(self.model, ordering.replace('-', '')):
            return ordering

        return super(MovieListPageView, self).get_ordering()

    def get_queryset(self):
        queryset = super(MovieListPageView, self).get_queryset().prefetch_related('user')

        user_filter = self.request.GET.get('user')
        if user_filter:
            queryset = queryset.filter(user_id=user_filter)

        return queryset
