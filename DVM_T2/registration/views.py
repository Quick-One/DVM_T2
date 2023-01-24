from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import QuizUserForm, TestForm

def register(request):
    if request.method == 'POST':
        form = QuizUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f'Account created for {new_user.user.username}!')
            return redirect('login')
    else:
        form = QuizUserForm()
    return render(request, 'registration/register.html', {'form': form})

def google_register(request):
    if request.method == 'POST':
        form = QuizUserForm(request.POST, instance=request.user)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f'Account created for {new_user.user.username}!')
            return redirect('login')
    else:
        form = QuizUserForm()
    return render(request, 'registration/google_register.html', {'form': form})

def test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = TestForm()
    return render(request, 'registration/register.html', {'form': form})

def test2(request):
    return render(request, "registration/index.html")