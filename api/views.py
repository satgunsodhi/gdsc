from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import News, apiKey, Comment, Log
from .serializers import NewsSerializer, CommentSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from random import choice
# Create your views here.

def homepage(request):
    news = News.objects.all()
    context = {'news':news}
    Log(log_info = 'Home page was served to '+ str(request.user)).save()
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
            Log(log_info = 'User was logged in:'+str(user)).save()
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not match')
        
    context = {'page': page}
    Log(log_info = 'Login page was accessed').save()
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
        Log(log_info = 'user was logged in:'+str(user)).save()
        return redirect('home')
    
    Log(log_info = 'register page was accessed').save()
    return render(request, 'api/login_register.html', context)

def logoutUser(request):
    logout(request)
    Log(log_info = 'user logged out:'+str(request.user)).save()
    return redirect('home')

@api_view(['GET'])
def listnews(request,pk,apkey):
    apikeys= apiKey.objects.all()
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):
            news = News.objects.get(id=pk)
            news.views += 1
            news.save()
            serialized = NewsSerializer(news)
            Log(log_info = 'News number '+str(pk)+'was served to apikey '+apkey).save()
            return Response(serialized.data)
    Log(log_info = 'invalid api call was made with wrong apikey key: '+apkey).save()
    return Response({'error':'apikey dosent match'})

@api_view(['GET'])
def randomnews(request,apkey):
    apikeys= apiKey.objects.all()
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):
            rint = choice(list(News.objects.values_list('id')))
            news = News.objects.get(id=rint[0])
            news.views += 1
            news.save()
            serialized = NewsSerializer(news)
            Log(log_info = 'random news was served to api key'+apkey).save()
            return Response(serialized.data)
    Log(log_info = 'invalid api call was made with wrong apikey key: '+apkey).save()
    return Response({'error':'apikey dosent match'})

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
                    news.views += 1
                    news.save()
                    serialized += NewsSerializer(news)
                    return Response(serialized.data)
            else:
                return Response({'error':'No data matched'})
    Log(log_info = 'invalid api call was made with wrong apikey key: '+apkey).save()
    return Response({'error':'apikey dosent match'})

@api_view(['GET'])
def modenews(request,mode,apkey):
    apikeys= apiKey.objects.all()
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):
            if(mode == '1'):
                return getlatest(apkey)
            if(mode == '2'):
                return getpopular(apkey)
            if(mode == '3'):
                return getbest(apkey)
    Log(log_info = 'invalid api call was made with wrong apikey key: '+apkey).save()
    return Response({'error':'apikey dosent match'})



def getlatest(apkey):
    news = News.objects.all()
    nid = list(News.objects.values_list('id',flat=True))[0]
    for oid in list(News.objects.values_list('id',flat=True)):
        if News.objects.get(id=oid).updated > News.objects.get(id=nid).updated:
            nid = oid
    news = News.objects.get(id=nid)
    news.views += 1
    news.save()
    serialized = NewsSerializer(news)
    Log(log_info = 'latest news was served to api key '+apkey).save()
    return Response(serialized.data)

def getpopular(apkey):
    nid = list(News.objects.values_list('views',flat=True))[0]
    for oid in list(News.objects.values_list('id',flat=True)):
        if News.objects.get(id=oid).views > News.objects.get(id=nid).views:
            nid = oid
    news = News.objects.get(id=nid)
    news.views += 1
    news.save()
    News.objects.get(id=nid).views+=1
    serialized = NewsSerializer(news)
    Log(log_info = 'popular news was served to api key '+apkey).save()
    return Response(serialized.data)

def getbest(apkey):
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
    news.views += 1
    news.save()
    serialized = NewsSerializer(news)
    Log(log_info = 'best news was served to api key '+apkey).save()
    return Response(serialized.data)

@api_view(['GET'])
def showcomments(request,pk,apkey):
    apikeys= apiKey.objects.all()
    for ap in apikeys:
        ap = str(ap)
        apkey = str(apkey)
        if (apkey == ap):    
            comment = Comment.objects.filter()
            serealized = CommentSerializer(comment)
            Log(log_info = 'Comment no. '+str(pk)+'was accessed by apikey '+str(apkey)).save()
            return Response(serealized.data)
    Log(log_info = 'invalid api call was made with wrong apikey key: '+apkey).save()
    return Response({'error':'apikey dosent match'})