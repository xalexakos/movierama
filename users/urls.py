from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.user_registration_view, name='user_registration_view'),
]
