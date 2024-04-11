from django.urls import path
from . import views

urlpatterns = [
    path('', views.randomnews),
    path('list/<str:pk>', views.listnews),
    path('?data=<str:pk>', views.search),
    path('?mode=<str:pk>', views.modenews),
]