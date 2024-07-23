from django.db import models
from encprofiles.models import User

class PersonalChat(models.Model):
    first_participant = models.ForeignKey(User, related_name='as_first', on_delete=models.CASCADE)
    second_participant = models.ForeignKey(User, related_name='as_second', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    new_messages_number_for_first = models.IntegerField(default=0)
    new_messages_number_for_second = models.IntegerField(default=0)
    last_message = models.ForeignKey('PersonalMessage', null=True, on_delete=models.CASCADE)
    
class PersonalMessage(models.Model):
    chat = models.ForeignKey(PersonalChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    encrypted_message = models.TextField(max_length=4096)
    is_edited = models.BooleanField(default=False, blank=False)
    is_read = models.BooleanField(default=False, blank=False)
    is_deleted_for_receiver = models.BooleanField(default=False, blank=False)
    is_deleted_for_sender = models.BooleanField(default=False, blank=False)
    
