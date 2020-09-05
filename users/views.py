from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from users.decorators import anonymous_user
from users.forms import UserRegistrationForm


@anonymous_user
def user_registration_view(request):
    """ Register a new user and start a new session by redirecting to movies list page. """
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('movies_list_view')

    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def user_logout_view(request):
    """ Terminates user session and redirects to movies list page. """
    logout(request)
    return redirect('movies_list_view')


@anonymous_user
def user_login_view(request):
    form = AuthenticationForm()
    context = {'form': form}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'movies_list_view'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')

    return render(request, 'users/login.html', context)
