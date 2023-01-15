from django import forms
from django.contrib.auth.models import User
from registration.models import QuizUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=QuizUser.USER_TYPE_CHOICES)
