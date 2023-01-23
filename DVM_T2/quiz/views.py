from collections import deque

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User

from openpyxl import Workbook

from .forms import (ChooseQuestionTypeForm, NewMultipleChoiceQuestionForm,
                    NewNumQuestionForm, NewQuizForm, NewTFQuestionForm, get_form)
from .models import (Question, Questionaire, Response, get_response_class)


def get_unanswered_quizzes(user):
    answered_questions = user.response_set.all()
    answered_quizzes_id = set(
        [q.question.questionaire.pk for q in answered_questions])
    all_quizzes = Questionaire.objects.all()
    unanswered_quizzes = [
        q for q in all_quizzes if q.pk not in answered_quizzes_id]
    unanswered_quizzes = [
        q for q in unanswered_quizzes if len(q.question_set.all()) != 0]
    return unanswered_quizzes


def get_answered_quizzes(user):
    answered_questions = user.response_set.all()
    answered_quizzes_id = set(
        [q.question.questionaire.pk for q in answered_questions])
    return [Questionaire.objects.get(pk=q) for q in answered_quizzes_id]


@login_required
def home(request):
    return render(request, 'quiz/home.html')


@login_required
def new_quiz(request):
    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    if request.method == 'POST':
        form = NewQuizForm(request.POST)
        if form.is_valid():
            new_quiz = form.save(commit=False)
            new_quiz.author = request.user
            new_quiz.save()
            messages.success(request, f'New quiz created!')
            return redirect('quiz-detail', pk=new_quiz.pk)
    else:
        form = NewQuizForm()
    return render(request, 'quiz/new_quiz.html', {'form': form})


@login_required
def show_quizzes(request):
    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    questionaires = Questionaire.objects.filter(author=request.user)
    size = len(questionaires)
    return render(request, 'quiz/quiz.html', {'questionaires': questionaires, 'size': size})


@login_required
def quiz_delete(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    # Deny access if user is not the author of the quiz
    questionaire = Questionaire.objects.get(pk=pk)
    if questionaire.author != request.user:
        raise PermissionDenied
    questionaire.delete()
    return redirect('quiz')


@login_required
def question_add(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    if request.method == 'POST':
        form = ChooseQuestionTypeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            question_type = form_data.get('question_type')
            if question_type == 'TF':
                return redirect('tf-add', pk=pk)
            elif question_type == 'NUM':
                return redirect('num-add', pk=pk)
            elif question_type == 'MCQ':
                return redirect('mcq-add', pk=pk)
    else:
        form = ChooseQuestionTypeForm()
    return render(request, 'quiz/new_quiz.html', {'form': form})


@login_required
def new_multiple_choice(request, pk):
    if request.method == 'POST':
        form = NewMultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.questionaire = Questionaire.objects.get(pk=pk)
            new_question.save()
            messages.success(request, f'New question added!')
            return redirect('quiz-detail', pk=pk)
    else:
        form = NewMultipleChoiceQuestionForm()
    return render(request, 'quiz/new_quiz.html', {'form': form})


@login_required
def new_true_false(request, pk):
    if request.method == 'POST':
        form = NewTFQuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.questionaire = Questionaire.objects.get(pk=pk)
            new_question.save()
            messages.success(request, f'New question added!')
            return redirect('quiz-detail', pk=pk)
    else:
        form = NewTFQuestionForm()
    return render(request, 'quiz/new_quiz.html', {'form': form})


@login_required
def new_numerical(request, pk):
    if request.method == 'POST':
        form = NewNumQuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.questionaire = Questionaire.objects.get(pk=pk)
            new_question.save()
            messages.success(request, f'New question added!')
            return redirect('quiz-detail', pk=pk)
    else:
        form = NewNumQuestionForm()
    return render(request, 'quiz/new_quiz.html', {'form': form})


@login_required
def quiz_detail(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    # allow access only if user is the author of the quiz
    if request.user != Questionaire.objects.get(pk=pk).author:
        raise PermissionDenied

    questionaire = Questionaire.objects.get(pk=pk)
    questions = questionaire.question_set.all()
    return render(request, 'quiz/quiz_detail.html', {'questions': questions,
                                                     'size': len(questions), 'pk': pk, 'quiz': questionaire})


@login_required
def question_delete(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    # Deny access if user is not the author of the quiz
    question = Question.objects.get(pk=pk)
    questionaire = question.questionaire

    if questionaire.author != request.user:
        raise PermissionDenied
    question.delete()
    return redirect('quiz-detail', pk=questionaire.pk)


@login_required
def question_edit(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied

    question = Question.objects.get(pk=pk).TypedQuestion
    qtype = question.type
    questionaire = question.questionaire

    # Deny access if user is not the author of the quiz
    if questionaire.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = get_form(qtype)(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, f'Question updated!')
            return redirect('quiz-detail', pk=questionaire.pk)
    else:
        form = get_form(qtype)(instance=question)
    return render(request, 'quiz/new_quiz.html', {'form': form})


@login_required
def active_quizzes(request):
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    questionaires = get_unanswered_quizzes(request.user)
    return render(request, 'quiz/active_quiz.html', {'questionaires': questionaires, 'size': len(questionaires)})


quiz_attempt_cache = {}


@login_required
def attempt_quiz(request, pk):

    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    if (request.user, pk) in quiz_attempt_cache:
        question_stack, response_list = quiz_attempt_cache[(request.user, pk)]

        if request.method == 'POST':
            question = question_stack.popleft()
            form = question.response_form()(request.POST)
            if form.is_valid():
                answer = form.cleaned_data.get('answer')
                print(answer)
                response_cls = get_response_class(question.type)
                response = response_cls(
                    question=question,
                    user=request.user,
                    answer=answer
                )
                response_list.append(response)
            else:
                return render(request, 'quiz/quiz_question.html', {'form': form, 'question': question})

        if len(question_stack) == 0:
            quiz_attempt_cache.pop((request.user, pk))
            print(response_list)
            for response in response_list:
                response.save()
            return redirect('quiz-result', pk=pk)
        question = question_stack[0]
        form = question.response_form()
        return render(request, 'quiz/quiz_question.html', {'form': form, 'question': question})

    # check if quiz is active
    if pk not in [q.pk for q in get_unanswered_quizzes(request.user)]:
        raise PermissionDenied

    questionaire = Questionaire.objects.get(pk=pk)
    questions = questionaire.question_set.all()
    questions = [q.TypedQuestion for q in questions]
    response_list = []
    question_stack = deque(questions)
    quiz_attempt_cache[(request.user, pk)] = (question_stack, response_list)
    return redirect('attempt-quiz', pk=pk)


@login_required
def quiz_result(request, pk):
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    if pk not in [q.pk for q in get_answered_quizzes(request.user)]:
        raise PermissionDenied

    quiz = Questionaire.objects.get(pk=pk)
    responses = Response.objects.filter(
        question__questionaire=quiz, user=request.user)
    responses = [r.TypedResponse for r in responses]
    context = {
        'responses': responses,
        'quiz': quiz,
        'score': sum([r.get_score() for r in responses]),
        'total': sum([r.question.reward for r in responses])
    }
    return render(request, 'quiz/quiz_result.html', context)


@login_required
def attempted_quizzes(request):
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    questionaires = get_answered_quizzes(request.user)
    return render(request, 'quiz/attempted.html', {'questionaires': questionaires, 'size': len(questionaires)})

@login_required
def scorebook(request, pk):
    response =  HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Scorebook.xlsx"'
    wb = Workbook()
    sheet = wb.active
    
    sheet.append(['Username', 'Score'])
    questionaire = Questionaire.objects.get(pk=pk)
    responders = Response.objects.filter(question__questionaire=questionaire).values_list('user', flat=True).distinct()
    for r in responders:
        responder = User.objects.get(pk=r)
        responses = Response.objects.filter(question__questionaire=questionaire, user=responder)
        responses = [r.TypedResponse for r in responses]
        score = sum([r.get_score() for r in responses])
        sheet.append([responder.username, score])
    
    wb.save(response)
    return response