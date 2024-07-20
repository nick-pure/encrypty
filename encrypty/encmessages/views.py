from django.shortcuts import render
from django.http import JsonResponse
from encprofiles.decorators import login_required
from .forms import PersonalChatForm, PersonalMessageForm
from encprofiles.models import User
from .models import PersonalMessage, PersonalChat

@login_required
def create_chat(request):
    if request.method == 'POST':
        try:
            data = request.POST
            user1 = User.objects.get(id=request.user.id)
            user2 = User.objects.get(id=data['id'])
            form = PersonalChatForm(participants=[user1, user2])
            if form.is_valid() and PersonalChat.objects:
                form.save()
                return JsonResponse({'status': 'ok', 'info': {'description': 'Chat is successfuly created'}}, status=200)
            else:
                return JsonResponse({'status': 'wrong', 'info': {'error': 'Data is invalid'}}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'status': 'wrong', 'info': {'error': 'The second user id is invalid'}}, status=401)

@login_required
def send_message(request):
    if request.method == 'POST':
        form = PersonalChatForm(request.POST)
    else:
        return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid HTTP method'}}, status=405)
