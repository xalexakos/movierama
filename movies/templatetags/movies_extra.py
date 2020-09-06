from django import template
from django.template.defaultfilters import safe

from movies.utils import get_response_query_params

register = template.Library()


@register.filter()
def pages_range(max_page):
    return range(1, max_page + 1)


@register.simple_tag
def get_vote_display(request, movie, vote):
    """ Format the appropriate vote url according to user authentication and movie creator. """
    votes_count = movie.total_likes if vote == 'like' else movie.total_hates
    if not votes_count:
        votes_count = 0

    votes_verbose = '%s %ss' % (votes_count, vote)
    if not request.user.is_authenticated or request.user.id == movie.user.id:
        return votes_verbose

    voted = getattr(movie, '%ss' % vote).users.filter(pk=request.user.id).exists()
    return safe(
        '<a class="%(class_name)s" href="/vote/%(movie_id)s/%(vote)s/%(url_search_params)s">%(verbose)s</a>' % {
            'verbose': votes_verbose,
            'movie_id': movie.id,
            'vote': vote,
            'url_search_params': get_response_query_params(request),
            'class_name': 'voted' if voted else ''
        }
    )
