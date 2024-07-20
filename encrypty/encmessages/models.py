from django.db import models
from encprofiles.models import User

class ChatPatricipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey('PersonalChat', related_name='participants', on_delete=models.CASCADE)

class PersonalChat(models.Model):
    participants = models.ManyToManyField(User, through=ChatPatricipant)
    created_at = models.DateTimeField(auto_now_add=True)
    new_messages_number_for_first = models.IntegerField(default=0)
    new_messages_number_for_second = models.IntegerField(default=0)
    last_message = models.ForeignKey('PersonalMessage', default=None)
    
class PersonalMessage(models.Model):
    chat = models.ForeignKey(PersonalChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    encrypted_message = models.TextField(max_length=4096)
    is_edited = models.BooleanField(default=False, blank=False)
    is_read = models.BooleanField(default=False, blank=False)
    is_deleted_for_receiver = models.BooleanField(default=False, blank=False)
    is_deleted_for_sender = models.BooleanField(default=False, blank=False)
    
