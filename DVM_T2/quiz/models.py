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
    option_C =  models.CharField(max_length=100)
    option_D = models.CharField(max_length=100)
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)
    def __str__(self):
        return self.question

    @property
    def get_options(self):
        return f'A. {self.option_A}\nB. {self.option_B}\nC. {self.option_C}\nD. {self.option_D}\nCorrect Answer: {self.answer}'

class Response(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=MCQ_TYPE_CHOICES)
    
    def __str__(self):
        return f'{self.responder},{self.question},{self.answer}'
    
    

admin.site.register(Questionaire)
admin.site.register(MCQuestion)
admin.site.register(Response)