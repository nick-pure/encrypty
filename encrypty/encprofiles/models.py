from django.db import models

class UserStatus(models.IntegerChoices):
    ACTIVE = 1
    OFF = 2

class User(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15)
    status = models.IntegerField(choices=UserStatus, default=UserStatus.ACTIVE)
    last_seen = models.TimeField(auto_now_add=True)
    # pic = models.ImageField()

