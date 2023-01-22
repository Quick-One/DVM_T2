from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class QuizUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    USER_TYPES = [
        ('QT', 'Quiz Taker'),
        ('QM', 'Quiz Maker'),
    ]
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
    )

    def __str__(self):
        return f'[{self.user_type}] {self.user.username}'

admin.site.register(QuizUser)