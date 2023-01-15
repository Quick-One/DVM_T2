from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewQuizForm, NewQuestion
from .models import Questionaire, MCQuestion, Response
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def get_unanswered_quizzes(user):
    answered_questions = user.response_set.all()
    answered_quizzes_id = set([q.question.questionaire.pk for q in answered_questions])
    all_quizzes = Questionaire.objects.all()
    unanswered_quizzes = [q for q in all_quizzes if q.pk not in answered_quizzes_id]
    return unanswered_quizzes

def get_answered_quizzes(user):
    answered_questions = user.response_set.all()
    answered_quizzes_id = set([q.question.questionaire.pk for q in answered_questions])
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
            form_data = form.cleaned_data
            title = form_data.get('title')
            description = form_data.get('description')
            author = request.user
            new_quiz = Questionaire(
                title=title, description=description, author=author)
            new_quiz.save()
            messages.success(request, f'New quiz created!')
            return redirect('quiz-detail', pk=new_quiz.pk)
    else:
        form = NewQuizForm()
    context = {
        'form': form
    }
    return render(request, 'quiz/new_quiz.html', context)


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
        form = NewQuestion(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            question = form_data.get('question')
            option_A = form_data.get('option_A')
            option_B = form_data.get('option_B')
            option_C = form_data.get('option_C')
            option_D = form_data.get('option_D')
            answer = form_data.get('answer')
            questionaire = Questionaire.objects.get(pk=pk)
            new_question = MCQuestion(questionaire=questionaire, question=question, option_A=option_A,
                                      option_B=option_B, option_C=option_C, option_D=option_D, answer=answer)
            new_question.save()
            messages.success(request, f'New question added!')
            return redirect('quiz-detail', pk=pk)
    else:
        form = NewQuestion()
    context = {
        'form': form
    }
    return render(request, 'quiz/new_quiz.html', context)


@login_required
def quiz_detail(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied
    
    #allow access only if user is the author of the quiz
    if request.user != Questionaire.objects.get(pk=pk).author:
        raise PermissionDenied

    questionaire = Questionaire.objects.get(pk=pk)
    questions = questionaire.mcquestion_set.all()
    return render(request, 'quiz/quiz_detail.html', {'questions': questions, 
    'size': len(questions), 'pk': pk, 'quiz': questionaire})

@login_required
def question_delete(request, pk):

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied
    
    # Deny access if user is not the author of the quiz
    question = MCQuestion.objects.get(pk=pk)
    questionaire = question.questionaire

    if questionaire.author != request.user:
        raise PermissionDenied
    question.delete()
    return redirect('quiz-detail', pk=questionaire.pk)

@login_required
def question_edit(request, pk):
    question = MCQuestion.objects.get(pk=pk)
    questionaire = question.questionaire

    if request.user.quizuser.user_type != 'QM':
        raise PermissionDenied
    # Deny access if user is not the author of the quiz
    if questionaire.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = NewQuestion(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            question.question = form_data.get('question')
            question.option_A = form_data.get('option_A')
            question.option_B = form_data.get('option_B')
            question.option_C = form_data.get('option_C')
            question.option_D = form_data.get('option_D')
            question.answer = form_data.get('answer')
            question.save()
            messages.success(request, f'Question edited!')
            return redirect('quiz-detail', pk=questionaire.pk)
    else:
        form = NewQuestion(initial={'question': question.question, 'option_A': question.option_A, 
        'option_B': question.option_B, 'option_C': question.option_C, 'option_D': question.option_D, 
        'answer': question.answer})
    context = {
        'form': form
    }
    return render(request, 'quiz/new_quiz.html', context)

@login_required
def active_quizzes(request):
    print("active quizzes")
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    questionaires = get_unanswered_quizzes(request.user)
    return render(request, 'quiz/active_quiz.html', {'questionaires': questionaires, 'size': len(questionaires)})


@login_required
def attempt_quiz(request, pk):
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    if pk not in [q.pk for q in get_unanswered_quizzes(request.user)]: #check if quiz is active
        raise PermissionDenied

    questionaire = Questionaire.objects.get(pk=pk)
    questions = questionaire.mcquestion_set.all()

    if request.method == 'POST':
        resp = list(dict(request.POST).values())[1:]
        for q, r in zip(questions, resp):
            new_response = Response(question=q, answer=r[0], responder=request.user)
            new_response.save()
        return redirect('quiz-result', pk=pk)
    return render(request, 'quiz/attempt_quiz.html', {'questions': questions, 'size': len(questions), 'pk': pk})

@login_required
def quiz_result(request, pk):
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    if pk not in [q.pk for q in get_answered_quizzes(request.user)]:
        raise PermissionDenied

    quiz = Questionaire.objects.get(pk=pk)
    responses = Response.objects.filter(question__questionaire=quiz, responder=request.user)
    return render(request, 'quiz/quiz_result.html', {'responses': responses, 'size': len(responses), 'quiz': quiz})

@login_required
def attempted_quizzes(request):
    if request.user.quizuser.user_type != 'QT':
        raise PermissionDenied

    questionaires = get_answered_quizzes(request.user)
    return render(request, 'quiz/attempted.html', {'questionaires': questionaires, 'size': len(questionaires)})