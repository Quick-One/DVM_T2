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
    private = models.BooleanField(default=False)
    PIN = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Question(models.Model):
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    reward = models.PositiveIntegerField(default=0)
    penalty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

    def check_answer(self, answer):
        return self.TypedQuestion.answer == answer

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

    def get_score(self):
        if self.question.check_answer(self.TypedResponse.answer):
            return self.question.reward
        else:
            return -self.question.penalty
    
    def description_dict(self):
        d = {}
        d['Question'] = self.question.question
        d['Your Answer'] = self.TypedResponse.answer
        d['Correct Answer'] = self.question.TypedQuestion.answer
        d['Score'] = f'{self.get_score()}/{self.question.reward}'
        return d

    @property
    def TypedResponse(self):
        try:
            return self.multiplechoiceresponse
        except MultipleChoiceResponse.DoesNotExist:
            pass
        try:
            return self.tfresponse
        except TFResponse.DoesNotExist:
            pass
        try:
            return self.numresponse
        except NumResponse.DoesNotExist:
            pass


class TFQuestion(Question):
    type = QType.TF
    answer = models.BooleanField()

    def response_form(self):
        class ResponseForm(forms.Form):
            answer = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=[(True, 'True'), (False, 'False')]
            )
        return ResponseForm

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
            choices = [
                ('A', self.option_A),
                ('B', self.option_B),
                ('C', self.option_C),
                ('D', self.option_D),
            ]
            answer = forms.CharField(
                widget=forms.RadioSelect(choices=choices)
            )
        return ResponseForm

    @property
    def description_dict(self):
        d = super().description_dict
        d['Answer'] = self.answer
        d['option_A'] = self.option_A
        d['option_B'] = self.option_B
        d['option_C'] = self.option_C
        d['option_D'] = self.option_D
        return d
    
    def get_option(self, option):
        if option == 'A':
            return self.option_A
        elif option == 'B':
            return self.option_B
        elif option == 'C':
            return self.option_C
        elif option == 'D':
            return self.option_D
        else:
            raise ValueError('Invalid option')


class MultipleChoiceResponse(Response):
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)

    def description_dict(self):
        d = super().description_dict()
        d['Your Answer'] = f"{self.answer}) {self.question.TypedQuestion.get_option(self.answer)} "  
        d['Correct Answer'] = f"{self.question.TypedQuestion.answer}) {self.question.TypedQuestion.get_option(self.question.TypedQuestion.answer)}"
        return d


def get_response_class(qtype):
    if qtype is QType.MCQ:
        return MultipleChoiceResponse
    elif qtype is QType.TF:
        return TFResponse
    elif qtype is QType.NUM:
        return NumResponse
    else:
        raise ValueError('Invalid question type')


admin.site.register(Questionaire)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(TFQuestion)
admin.site.register(TFResponse)
admin.site.register(NumQuestion)
admin.site.register(NumResponse)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceResponse)
