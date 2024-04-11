from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import News
from rest_framework import response
from .serializers import NewsSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def homepage(request):
    news = News.objects.all()
    context = {'news':news}
    return render(request, 'api/home.html', context)

@api_view(['GET'])
def listnews(request,pk):
    news = News.objects.get(id=pk)
    serialized = NewsSerializer(news)
    return Response(serialized)

@api_view(['GET'])
def randomnews(request):
    return Response({'name':'hello'})

@api_view(['GET'])
def search(request):
    return Response({'name':'hello'})

@api_view(['GET'])
def modenews(request):
    return Response({'name':'hello'})

def LoginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not match')

def register(request):
    form = UserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    
    if form.is_valid():
        user = form.save(commit = False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')
        
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')