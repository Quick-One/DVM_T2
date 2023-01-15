from django import forms
from .models import Questionaire, MCQuestion

class NewQuizForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500)

class NewQuestion(forms.ModelForm):
    class Meta:
        model = MCQuestion
        fields = ['question', 'option_A', 'option_B', 'option_C', 'option_D', 'answer']

