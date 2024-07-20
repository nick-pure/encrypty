from django.forms import ModelForm
from django import forms
from .models import ChatPatricipant, PersonalChat, PersonalMessage

class PersonalChatForm(ModelForm):
    class Meta:
        model = PersonalChat
        fields = ['patricipants']

class PersonalMessageForm(ModelForm):
    class Mets:
        model = PersonalMessage
        fields = ['encrypted_message']

