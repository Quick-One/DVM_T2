from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/new/', views.new_quiz, name='new'),
    path('quiz/<int:pk>/delete/', views.quiz_delete, name='quiz-delete'),
    path('quiz/<int:pk>/add/', views.question_add, name='question-add'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz-detail'),
    path('quiz/', views.show_quizzes, name='quiz'),
    path('question/<int:pk>/delete/', views.question_delete, name='question-delete'),
    path('question/<int:pk>/edit/', views.question_edit, name='question-edit'),
    path('attempt/<int:pk>/', views.attempt_quiz, name='attempt-quiz'),
    path('attempt/<int:pk>/result/', views.quiz_result, name='quiz-result'),
    path('active/', views.active_quizzes, name='active-quizzes'),
    path('attempted/', views.attempted_quizzes, name='attempted-quizzes'),
]