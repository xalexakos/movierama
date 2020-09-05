from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieListPageView.as_view(), name='movies_list_view'),
]
