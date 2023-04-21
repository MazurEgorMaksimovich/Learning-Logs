#Определяет схемы УРЫЛ для пользователей

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns =[
    #По умалчанию.
    path('', include('django.contrib.auth.urls')),
    #Страничка регистрации.
    path('register/', views.register, name='register'),
]