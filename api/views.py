from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import News
from rest_framework import response
from .serializers import NewsSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from random import randint
from .models import apiKey
# Create your views here.

def homepage(request):
    news = News.objects.all()
    context = {'news':news}
    return render(request, 'api/home.html', context)


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
        
    context = {'page': page}
    return render(request, 'api/login_register.html', context)

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
        
    return render(request, 'api/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@api_view(['GET'])
def listnews(request,pk,apkey):
    apikeys= apiKey.objects.all()
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):
            news = News.objects.get(id=pk)
            serialized = NewsSerializer(news)
            return Response(serialized.data)
    return Response({'error':'apikey dosent match'})

@api_view(['GET'])
def randomnews(request):
    return Response({'name':'hello'})

@api_view(['GET'])
def search(request,data,apkey):
    data = str(data)
    print(data)
    apikeys= apiKey.objects.all()
    nid = []
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):
            for oid in list(News.objects.values_list('id',flat=True)):
                if data in News.objects.get(id=oid).content:
                    nid.append(oid)
            print(nid)
            if nid:
                serializer = NewsSerializer(News.objects.get(id=nid[0]))
                for i in nid[1:]:
                    news = News.objects.get(id=i)
                    serialized += NewsSerializer(news)
                    return Response(serialized.data)
            else:
                return Response({'error':'No data matched'})
    return Response({'error':'apikey dosent match'})

@api_view(['GET'])
def modenews(request,mode,apkey):
    apikeys= apiKey.objects.all()
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):
            if(mode == '1'):
                return getlatest()
            if(mode == '2'):
                return getpopular()
            if(mode == '3'):
                return getbest()

    return Response({'error':'apikey dosent match'})

@api_view(['GET'])
def listerror(request):
    return Response({'name':'hello'})


def getlatest():
    news = News.objects.all()
    nid = list(News.objects.values_list('id',flat=True))[0]
    for oid in list(News.objects.values_list('id',flat=True)):
        if News.objects.get(id=oid).updated > News.objects.get(id=nid).updated:
            nid = oid
    news = News.objects.get(id=nid)
    serialized = NewsSerializer(news)
    return Response(serialized.data)

def getpopular():
    nid = list(News.objects.values_list('views',flat=True))[0]
    for oid in list(News.objects.values_list('id',flat=True)):
        if News.objects.get(id=oid).views > News.objects.get(id=nid).views:
            nid = oid
    news = News.objects.get(id=nid)
    serialized = NewsSerializer(news)
    return Response(serialized.data)

def getbest():
    nid = 0
    best = 0
    for oid in list(News.objects.values_list('id',flat=True)):
        print()
        criteria = 0.3*int(News.objects.get(id=oid).updated.hour+News.objects.get(id=oid).updated.minute/60+News.objects.get(id=oid).updated.second/3600) + 0.7*int(News.objects.get(id=oid).views)
        if oid == nid:
            continue
        if criteria > best:
            nid = oid
            best = criteria
    news = News.objects.get(id=nid)
    serialized = NewsSerializer(news)
    return Response(serialized.data)

def showcomments():
    return True