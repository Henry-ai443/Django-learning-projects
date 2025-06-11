from django.shortcuts import render, redirect
from .models import Topic, Entry
from django.http import Http404
from .forms import TopicForm, EntryForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

@login_required
def topic(request, pk):
    topic = Topic.objects.get(pk = pk)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('topics')
        
    context = {'form': form}
    return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, pk):
    topic = Topic.objects.get(pk = pk)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('topics')
        
    context = {'topic': topic, 'form': form}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm( request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('topics')
        
    context = {
        'entry': entry,
        'topic': topic,
        'form':form
    }

    return render(request, 'edit_entry.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            raw_password = request.POST.get('password1')
            authenticated_user = authenticate(username = new_user.username, password = raw_password)
            login(request, authenticated_user)
            return redirect('index')
    context = {'form': form}
    return render(request, 'register.html', context)