import uuid

from django.db import models
from encprofiles.models import User

class PersonalChat(models.Model):
    first_participant = models.ForeignKey(User, related_name='as_first', on_delete=models.CASCADE)
    second_participant = models.ForeignKey(User, related_name='as_second', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    new_messages_number_for_first = models.IntegerField(default=0)
    new_messages_number_for_second = models.IntegerField(default=0)
    last_message_for_first = models.ForeignKey('PersonalMessage', related_name='as_first', null=True, on_delete=models.CASCADE)
    last_message_for_second = models.ForeignKey('PersonalMessage', related_name='as_second', null=True, on_delete=models.CASCADE)
    
class PersonalMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(PersonalChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    encrypted_message = models.TextField(max_length=4096)
    is_edited = models.BooleanField(default=False, blank=False)
    is_read = models.BooleanField(default=False, blank=False)
    is_deleted_for_receiver = models.BooleanField(default=False, blank=False)
    is_deleted_for_sender = models.BooleanField(default=False, blank=False)

    def get_available_date(self):
        response = dict()
        response['id'] = self.id
        response['is_edited'] = self.is_edited
        response['is_read'] = self.is_read
        response['is_deleted_for_receiver'] = self.is_deleted_for_receiver
        response['is_deleted_for_sender'] = self.is_deleted_for_sender
        response['created_at'] = self.created_at.isoformat().split('T')[1].split('.')[0][:-3]
        response['encrypted_message'] = self.encrypted_message
        response['sender'] = str(self.sender.id)
        return response
    
