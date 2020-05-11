from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .forms import FeedbackForm
# Create your views here.

def home(request):
    return render(request, 'feedback/home.html')

def createuser(request):
    if request.method == 'GET':
        return render(request, 'feedback/createuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('givereview')
            except IntegrityError:
                return render(request, 'feedback/createuser.html', {'form': UserCreationForm(), 'error': 'Username already exists'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'feedback/loginuser.html', {'form': AuthenticationForm()})
    else:
        try:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user == None:
                return render(request, 'feedback/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username or password incorrect'})
            else:
                login(request, user)
                return redirect('givereview')
        except ValueError:
            return render(request, 'feedback/loginuser.html', {'form': AuthenticationForm(), 'error': 'Bad data entered'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def givereview(request):
    if request.method == 'GET':
        return render(request, 'feedback/givereview.html', {'form': FeedbackForm()})
    else:
        try:
            feedback = FeedbackForm(request.POST)
            input = feedback.save(commit=False)
            input.user = request.user
            analyser = pickle.load( open("feedback/dataset.dat", "rb"))
            score = analyser.polarity_scores(input.review)
            #print(score)
            input.feedback = score
            input.save()
            logout(request)

            return redirect('home')
        except ValueError:
            return render(request, 'feedback/givereview.html', {'form': FeedbackForm(), 'error': 'Bad data entered'})
