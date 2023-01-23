from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/new/', views.new_quiz, name='new'),
    path('quiz/<int:pk>/delete/', views.quiz_delete, name='quiz-delete'),
    path('quiz/<int:pk>/scorebook/', views.scorebook, name='scorebook'),
    path('quiz/<int:pk>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('quiz/<int:pk>/add/MCQ/', views.new_multiple_choice, name='mcq-add'),
    path('quiz/<int:pk>/add/TF/', views.new_true_false, name='tf-add'),
    path('quiz/<int:pk>/add/Num/', views.new_numerical, name='num-add'),
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
