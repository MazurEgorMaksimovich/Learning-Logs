from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """Главная домашняя страница приложения Лёрнинглог."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну из тем."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner, request.user)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Добавление новой темы."""
    if request.method != 'POST':
        #Создаётся пустая форма.
        form = TopicForm()
    else:
        #Обработка данных формы.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect(reverse('learning_logs:topics'))
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Добавление новой заметки."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #Создаётся пустая форма.
        form = EntryForm()
    else:
        #Обработка данных формы.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            check_topic_owner(topic.owner, request.user)
            new_entry_object = form.save(commit=False)
            new_entry_object.topic = topic
            new_entry_object.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редактирование заметки."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic.owner, request.user)

    if request.method != 'POST':
        #Создаётся пустая форма.
        form = EntryForm(instance=entry)
    else:
        #Обработка данных формы.
        form = EntryForm(instance=entry ,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(owner, user):
    """Проверяет пользователя на наличие права собственности на данную страницу."""
    if owner != user:
        raise Http404