import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from chat_app.constants import CHAT_NAME_PREFIX
from chat_app.forms import CreateChatForm, LoginForm
from chat_app.models import Chat, Message


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Login view
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(request=request, email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("index")
            except AttributeError:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'chat_app/auth.html', {'form': form, 'auth_form_action': 'Login'})


# Create your views here.
@login_required(login_url='/chat/login/')
def chat_view(request: HttpRequest) -> HttpResponse:
    """
    Main page view
    :param request:
    :return:
    """
    if request.method == "POST":
        form = CreateChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            return redirect('chat_room', chat_id=chat.id)
    else:
        form = CreateChatForm()
    chat_list = Chat.objects.filter(users=request.user)
    return render(request, 'chat_app/index.html', {'chat_list': chat_list, 'form': form})


@login_required(login_url='/chat/login/')
def chat_room_view(request: HttpRequest, chat_id: int) -> HttpResponse:
    """
    Chat page view
    :param request:
    :param chat_id:
    :return:
    """
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)
    return render(request, 'chat_app/room.html', {"chat": chat, "messages": messages})


@login_required(login_url='/chat/login/')
def edit_chat_room(request: HttpRequest, chat_id: int) -> HttpResponse:
    """
    Edit chat name and participants
    :param request:
    :param chat_id:
    :return:
    """
    chat = Chat.objects.filter(id=chat_id).first()
    if request.method == "POST":
        form = CreateChatForm(request.POST, instance=chat)
        if form.is_valid():
            chat = form.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'{CHAT_NAME_PREFIX}{chat_id}', {
                'type': 'chat_message',
                'message': f'Changed chat name: {chat.name}',
                'username': 'SYSTEM',
                'created_at': datetime.datetime.now().strftime("%H:%M %m %d, %Y"),
            })
            return redirect('chat_room', chat_id=chat.id)
    else:
        form = CreateChatForm(instance=chat)
    return render(request, 'chat_app/edit_chat.html', {"room_name": chat_id, 'form': form})
