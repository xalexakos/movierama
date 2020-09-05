from django.contrib.auth import login
from django.shortcuts import render, redirect

from users.forms import UserRegistrationForm


def user_registration_view(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('/')

    context = {'form': form}
    return render(request, 'users/registration.html', context)
