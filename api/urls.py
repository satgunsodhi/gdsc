from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.randomnews),
    path('api/list/<str:pk>/?apikey=<str:apkey>', views.listnews),
    path('api/news/?data=<str:pk>/?apikey=<str:apkey>', views.search),
    path('api/news/?mode=<str:pk>/?apikey=<str:apkey>', views.modenews),
    path('', views.homepage)
]