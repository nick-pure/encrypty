from django.shortcuts import render
from django.http import JsonResponse
from encprofiles.decorators import login_required
from .forms import PersonalChatForm, PersonalMessageForm
from encprofiles.models import User
from .models import PersonalMessage, PersonalChat, Membership

@login_required
def get_chat(request):
    if request.method == 'GET':
        data = request.GET
        chat_id = data['chat_id']
        try:
            PersonalChat.objects.get(id=chat_id)
            messages = PersonalMessage.objects.filter(chat=chat_id)
            return JsonResponse({'status': 'ok', 'messages': messages.all()}, status=200)
        except PersonalChat.DoesNotExist:
            return JsonResponse({'status': 'wrong', 'info': {'error': 'Personal chat doesn\'n exist'}}, status=404)
    else:
        return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid HTTP method'}}, status=405)

@login_required
def send_message(request):
    if request.method == 'POST':
        data = request.POST
        first_user = data['user_id']
        second_user = request.user
        try:
            first_user = User.objects.get(id=first_user)
        except User.DoesNotExist:
            return JsonResponse({'status': 'wrong', 'info': {'error': 'User doesn\'t exist'}}, status=405)

        first_chats = Membership.objects.filter(user=first_user).values_list('chat')
        second_chats = Membership.objects.filter(user=second_user).values_list('chat')
        chat_id = set(first_chats).intersection(second_chats)
        if len(chat_id) == 0:
            chat_id = PersonalChatForm(participants=[first_user, second_user])
        message = PersonalMessageForm({'encrypted_message' : data['message'], 'chat' : chat_id, 'sender' : second_user})
        message.save()
        return JsonResponse({'status': 'ok', 'info' : {'description' : 'Message is successfuly sent'}}, status=200)
    else:
        return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid HTTP method'}}, status=405)

