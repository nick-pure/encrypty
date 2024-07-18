from django.db import models
from encprofiles.models import User

class PersonalChat(models.Model):
    first_user = models.ManyToManyField(User)

class StatusOfMessages(models.IntegerChoices):
    # to manage status of message we need to add number of user(where 1 - is sender, and 2 - is receiver)
    NORMAL = 0
    DELETED_ON_SENDER_SIDE = 1
    DELETED_ON_RECEIVER_SIDE = 2
    DELETED = 3 
    
class PersonalMessage(models.Model):
    chat = models.ForeignKey(PersonalChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now_add=True)
    encrypted_message = models.TextField(max_length=4096)
    changed = models.BooleanField(default=False)
    status = models.IntegerField(choices=StatusOfMessages, default=StatusOfMessages.NORMAL)