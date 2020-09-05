from django.forms import ModelForm

from movies.models import Movie


class MovieCreateForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'user')
