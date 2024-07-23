from django.shortcuts import render
from django.http import JsonResponse
from encprofiles.decorators import login_required
from .forms import PersonalChatForm, PersonalMessageForm
from encprofiles.models import User
from django.db.models import Q
from .models import PersonalMessage, PersonalChat
from .responses import Ok, Er, Data
from .checker import single_way_check

class Chatter:
    @classmethod
    def read(self, messages, chat_id, receiver):
        new_messages = messages.filter(chat_id=chat_id).filter(~Q(sender=receiver)).filter(is_read=False)
        new_messages.update(is_read=True)
    
    @classmethod
    def consist(self, chat_id, first_id):
        chat = PersonalChat.objects.get(id=chat_id)
        first_user = User.objects.get(id=first_id)
        if chat.first_participant == first_user or chat.second_participant == first_user:
            return True
        else:
            return False

@login_required
@single_way_check('chat_id')
def get_chat(request):
    if request.method == 'GET':
        data = request.GET
        chat_id = data['chat_id']
        try:
            chat = PersonalChat.objects.get(id=chat_id)
            if not Chatter.consist(chat_id, request.user.id):
                return Er('Personal chat doesn\'n exist', 404)
            messages = PersonalMessage.objects.filter(chat=chat)
            Chatter.read(messages, chat_id, request.user)
            return Data({'messages' : list(messages.values())}, 200)
        except PersonalChat.DoesNotExist:
            return Er('Personal chat doesn\'n exist', 404)
    else:
        return Er('Invalid HTTP method', 405)

@login_required
def send_message(request):
    if request.method == 'POST':
        data = request.POST
        second_user = request.user
        encrypted_message = data['message']
        if 'user_id' in dict(data):
            first_user = data['user_id']
            try:
                chat_id = PersonalChat.objects.filter(first_participant=first_user).get(second_participant=second_user)
            except PersonalChat.DoesNotExist:
                try:
                    chat_id = PersonalChat.objects.filter(second_participant=first_user).get(first_participant=second_user)
                except PersonalChat.DoesNotExist:
                    chat_id = PersonalChatForm({'first_participant' : first_user, 'second_participant' : second_user})
                    chat_id.save()
                    chat_id = PersonalChat.objects.filter(first_participant=first_user).get(second_participant=second_user)
            chat_id = chat_id.id
        elif 'chat_id' in dict(data):
            chat_id = data['chat_id']
            try: 
                PersonalChat.objects.get(chat_id=chat_id)
                if not Chatter.consist(chat_id, request.user.id):
                    return Er('Chat doesn\'t exist', 404)
            except PersonalChat.DoesNotExist:
                return Er('Chat doesn\'t exist', 404)
        else:
            return Er('Invalid request', 400)
        message = PersonalMessageForm({'encrypted_message' : encrypted_message, 'chat' : chat_id, 'sender' : second_user})
        message.save()
        return Ok('Message is successfuly sent', 200)
    else:
        return Er('Invalid HTTP method', 405)

