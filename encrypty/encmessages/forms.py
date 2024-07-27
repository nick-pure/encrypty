from django.forms import ModelForm
from django import forms
from .models import PersonalChat, PersonalMessage

class PersonalChatForm(ModelForm):
    class Meta:
        model = PersonalChat
        fields = ['first_participant', 'second_participant']

class PersonalMessageForm(ModelForm):
    class Meta:
        model = PersonalMessage
        fields = ['encrypted_message', 'chat', 'sender']

