from enum import Enum

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


class QType(Enum):
    MCQ = 'Multiple Choice'
    TF = 'True/False'
    NUM = 'Numerical'


class Questionaire(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    reward = models.PositiveIntegerField(default=0)
    penalty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

    @property
    def TypedQuestion(self):
        try:
            return self.multiplechoicequestion
        except MultipleChoiceQuestion.DoesNotExist:
            pass
        try:
            return self.tfquestion
        except TFQuestion.DoesNotExist:
            pass
        try:
            return self.numquestion
        except NumQuestion.DoesNotExist:
            pass
        
    @property
    def description_dict(self):
        return {
            'Type': self.type.value,
            'Question': self.question,
            'Reward': self.reward,
            'Penalty': self.penalty,
        }



class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.question.question}'

    def check_answer(self, answer):
        return self.question.TypedQuestion.check_answer(answer)


class TFQuestion(Question):
    type = QType.TF
    answer = models.BooleanField()

    def response_form(self):
        class ResponseForm(forms.Form):
            answer = forms.BooleanField(
                widget=forms.RadioSelect(
                    choices=[(True, 'True'), (False, 'False')])
            )
        return ResponseForm

    def check_answer(self, answer):
        return self.answer == answer
    
    @property
    def description_dict(self):
        d = super().description_dict
        d['Answer'] = self.answer
        return d



class TFResponse(Response):
    answer = models.BooleanField()


class NumQuestion(Question):
    type = QType.NUM
    answer = models.IntegerField()

    def response_form(self):
        class ResponseForm(forms.Form):
            answer = forms.IntegerField()
        return ResponseForm

    def check_answer(self, answer):
        return self.answer == answer
    
    @property
    def description_dict(self):
        d = super().description_dict
        d['Answer'] = self.answer
        return d

    


class NumResponse(Response):
    answer = models.IntegerField()


MCQ_TYPE_CHOICES = [
    ('A', 'Option A'),
    ('B', 'Option B'),
    ('C', 'Option C'),
    ('D', 'Option D'),
]


class MultipleChoiceQuestion(Question):
    type = QType.MCQ
    option_A = models.CharField(max_length=100)
    option_B = models.CharField(max_length=100)
    option_C = models.CharField(max_length=100)
    option_D = models.CharField(max_length=100)
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)

    def response_form(self):
        class ResponseForm(forms.Form):
            answer = forms.CharField(
                widget=forms.RadioSelect(choices=MCQ_TYPE_CHOICES)
            )
        return ResponseForm

    def check_answer(self, answer):
        return self.answer == answer

    @property
    def description_dict(self):
        d = super().description_dict
        d['Answer'] = self.answer
        d['option_A'] = self.option_A
        d['option_B'] = self.option_B
        d['option_C'] = self.option_C
        d['option_D'] = self.option_D
        return d

class MultipleChoiceResponse(Response):
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)


admin.site.register(Questionaire)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(TFQuestion)
admin.site.register(TFResponse)
admin.site.register(NumQuestion)
admin.site.register(NumResponse)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceResponse)
