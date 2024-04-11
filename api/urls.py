from django.urls import path, include
from rest_framework.response import Response
from . import views

urlpatterns = [
    path('api/apikey=<str:apkey>', views.randomnews),
    path('list/<int:pk>/apikey=<str:apkey>', views.listnews),
    path('comment/<int:pk>', views.showcomments),
    path('api/news/data=<str:data>/apikey=<str:apkey>', views.search),
    path('api/news/mode=<str:mode>/apikey=<str:apkey>', views.modenews),
    path('', views.homepage, name = 'home'),
    path('login/', views.LoginPage, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logoutUser, name='logout'),
]