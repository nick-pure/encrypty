from django.db import models

class UserStatus(models.IntegerChoices):
    ACTIVE = 1
    OFF = 2

class User(models.Model):
    name = models.CharField(max_length=61, blank=False)
    description = models.CharField(max_length=255, blank=True)

    username = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=31, blank=False)
    is_hidden_phone = models.BooleanField(default=True)
    email = models.EmailField(blank=True)
    is_hidden_email = models.BooleanField(default=True)
    password = models.CharField(max_length=63)

    created = models.DateTimeField(auto_now_add=True)
    
    status = models.IntegerField(choices=UserStatus, default=UserStatus.ACTIVE)
    last_seen = models.TimeField(auto_now_add=True)
    # pic = models.ImageField()

    def get_all_data():
        pass

