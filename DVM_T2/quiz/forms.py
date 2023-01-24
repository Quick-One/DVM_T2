from django import forms
from .models import MultipleChoiceQuestion, TFQuestion, NumQuestion, Questionaire, QType

class NewQuizForm(forms.ModelForm):
    class Meta:
        model = Questionaire
        fields = ['title', 'description', 'private', 'PIN']
    
    def save(self, commit=True):
        quiz = super().save(commit=False)
        if commit:
            quiz.save()
        return quiz

class ChooseQuestionTypeForm(forms.Form):
    question_type = forms.ChoiceField(
        choices=[('TF', 'True/False'), ('NUM', 'Numerical'), ('MCQ', 'Multiple Choice')]
    )

class NewTFQuestionForm(forms.ModelForm):
    class Meta:
        model = TFQuestion
        fields = ['question', 'reward', 'penalty', 'answer']
        widgets = {
            'answer': forms.RadioSelect(choices=[(True, 'True'), (False, 'False')])
        }

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
        return question

class NewNumQuestionForm(forms.ModelForm):
    class Meta:
        model = NumQuestion
        fields = ['question', 'reward', 'penalty', 'answer']
    
    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
        return question

class NewMultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['question', 'reward', 'penalty', 'option_A', 'option_B', 'option_C', 'option_D', 'answer']
        
    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
        return question

class PINForm(forms.Form):
    PIN = forms.IntegerField()

def get_form(question_type):
    if question_type is QType.TF:
        return NewTFQuestionForm
    elif question_type is QType.NUM:
        return NewNumQuestionForm
    elif question_type is QType.MCQ:
        return NewMultipleChoiceQuestionForm
    else:
        raise ValueError('Invalid question type')
