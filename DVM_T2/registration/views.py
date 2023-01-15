from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizUser
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            new_user = form.save()
            new_quiz_user = QuizUser(user=new_user, user_type=form.cleaned_data.get('user_type'))
            new_quiz_user.save()

            messages.success(request, f'Account created for {new_user.username}!')
            
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})