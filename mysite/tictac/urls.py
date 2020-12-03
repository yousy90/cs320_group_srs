from django.urls import path

from . import views

app_name = 'tictac'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('entergame/', views.entergame, name='entergame')
    #path('siteerror/', views.siteerror, name='siteerror')
]
