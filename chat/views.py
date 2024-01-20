from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Chat, ChatMessage
from django.db.models import Q


@login_required
def index(request):
    chats = Chat.objects.filter(user1=request.user) | Chat.objects.filter(user2=request.user)
    return render(request, 'chat/index.html', {'chats': chats})


@login_required
def chat(request, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    messages = ChatMessage.objects.filter(chat_id=chat_id)
    return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'chat/signup.html', {'form': form})


@login_required
def users(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        chat = Chat.objects.filter(
            Q(user1=request.user, user2_id=user_id) | Q(user1_id=user_id, user2=request.user)
            ).first()
        
        if not chat:
            chat = Chat.objects.create(user1=request.user, user2_id=user_id)
        return redirect('/')
    
    return render(request, 'chat/users.html', {'users': users})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))



