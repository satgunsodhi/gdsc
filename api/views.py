from django.shortcuts import render
from rest_framework.response import Response
from .models import News
from rest_framework import response
from .serializers import NewsSerializer
from rest_framework.decorators import api_view
# Create your views here.

def homepage(request):
    return render(request, 'api/home.html')

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