from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import QuizUser


class QuizUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=QuizUser.USER_TYPES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']

    def save(self):
        user = super().save()
        quiz_user = QuizUser(
            user=user,
            user_type=self.cleaned_data['user_type']
        )
        quiz_user.save()
        return quiz_user

# class TestForm(forms.Form):
#     title = forms.MultipleChoiceField(
#         choices=QuizUser.USER_TYPES,
#         widget=forms.CheckboxSelectMultiple,
#     )


class TestForm(forms.Form):
    title = forms.BooleanField()
