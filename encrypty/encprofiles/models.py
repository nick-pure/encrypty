import uuid

from django.db import models


class UserStatus(models.IntegerChoices):
    ACTIVE = 1
    OFF = 2

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=61, blank=False)
    description = models.CharField(max_length=255, blank=True)

    username = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=15, blank=False)
    is_shown_phone = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    is_shown_email = models.BooleanField(default=False)
    password = models.CharField(max_length=63)

    created = models.DateTimeField(auto_now_add=True)
    
    status = models.IntegerField(choices=UserStatus, default=UserStatus.ACTIVE)
    last_seen = models.TimeField(auto_now_add=True)
    # pic = models.ImageField()

    def get_all_data(self):
        resp = dict()
        resp['username'] = self.username
        if self.is_shown_email:
            resp['email'] = self.email
        resp['name'] = self.name
        if self.is_shown_phone:
            resp['phone'] = self.phone
        resp['description'] = self.description
        resp['status'] = self.status
        if self.status != UserStatus.ACTIVE:
            resp['last_seen'] = self.last_seen
        resp['created'] = self.created
        resp['id'] = self.id
        return resp

