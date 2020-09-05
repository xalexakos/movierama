from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.decorators import anonymous_user
from users.forms import UserRegistrationForm


@anonymous_user
def user_registration_view(request):
    """ Register a new user and start a new session by redirecting to index page. """
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
    """ Terminates user session and redirects to index page. """
    logout(request)
    return redirect('movies_list_view')
