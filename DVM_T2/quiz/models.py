from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms


class Questionaire(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


MCQ_TYPE_CHOICES = [
    ('A', 'Option A'),
    ('B', 'Option B'),
    ('C', 'Option C'),
    ('D', 'Option D'),
]


class MCQuestion(models.Model):
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    option_A = models.CharField(max_length=100)
    option_B = models.CharField(max_length=100)
    option_C = models.CharField(max_length=100)
    option_D = models.CharField(max_length=100)
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)

    def __str__(self):
        return self.question

    @property
    def get_options(self):
        return f'A. {self.option_A}\nB. {self.option_B}\nC. {self.option_C}\nD. {self.option_D}\nCorrect Answer: {self.answer}'

    def response_form(self):
        choices = [('A', self.option_A), ('B', self.option_B),
                   ('C', self.option_C), ('D', self.option_D)]

        class ResponseForm(forms.Form):
            answer = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect
            )
        return ResponseForm


class Response(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)

    def __str__(self):
        return f'{self.responder},{self.question},{self.answer}'


# Creating a base Question class for all types of questions
# class Question(models.Model):
#     questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
#     question = models.CharField(max_length=500)
#     rewards = models.IntegerField(default=0)
#     penalty = models.IntegerField(default=0)

#     def __str__(self):
#         return self.question

# class MCQuestion(Question):
#     option_A = models.CharField(max_length=100)
#     option_B = models.CharField(max_length=100)
#     option_C =  models.CharField(max_length=100)
#     option_D = models.CharField(max_length=100)
#     answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)

#     def __str__(self):
#         return self.question

#     @property
#     def get_options(self):
#         return f'A. {self.option_A}\nB. {self.option_B}\nC. {self.option_C}\nD. {self.option_D}\nCorrect Answer: {self.answer}'

# # Creating a true/false question class
# class TFQuestion(Question):
#     answer = models.BooleanField()

#     def __str__(self):
#         return self.question

# # Creating a numeric question class
# class NumQuestion(Question):
#     answer = models.IntegerField()

#     def __str__(self):
#         return self.question

admin.site.register(Questionaire)
admin.site.register(MCQuestion)
admin.site.register(Response)
