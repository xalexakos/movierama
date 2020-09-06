from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieListPageView.as_view(), name='movies_list_view'),
    path('add-movie/', login_required(views.MovieAddPageView.as_view()), name='movies_add_view'),
    path('vote/<int:movie_id>/<str:vote>/', views.MovieVoteView.as_view(), name='movies_vote_view')
]
