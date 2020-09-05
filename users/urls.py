from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.user_registration_view, name='user_registration_view'),
    path('logout/', views.user_logout_view, name='user_logout_view'),
    path('login/', views.user_login_view, name='user_login_view'),
]
