"""Схемы ЮРЛь для лёрнинг-логс."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    #Home page.
    path('', views.index, name='index'),
    #Перечисляем темы.
    path('topics/', views.topics, name='topics'),
    #Страница с подробной информацией по отдельной теме.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    #Cтраница для добавления тем.
    path('new_topic/', views.new_topic, name='new_topic'),
    #Cтраница для добавления заметок.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #Страница для редактирования заметки.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]