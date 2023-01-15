from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.
class QuizUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    QUIZTAKER = 'QT'
    QUIZMAKER = 'QM'
    USER_TYPE_CHOICES = [
        (QUIZTAKER, 'Quiz Taker'),
        (QUIZMAKER, 'Quiz Maker'),
    ]
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPE_CHOICES,
    )

    def __str__(self):
        return f'{self.user_type} {self.user.username}'

admin.site.register(QuizUser)