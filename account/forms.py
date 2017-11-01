from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class Register(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)
