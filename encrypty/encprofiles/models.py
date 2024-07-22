from typing import Any
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)


class UserStatus(models.IntegerChoices):
    ACTIVE = 1
    OFF = 2
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=61, blank=False)
    description = models.CharField(max_length=255, blank=True)

    username = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=15, blank=False, unique=True)
    is_shown_phone = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    is_shown_email = models.BooleanField(default=False)
    password = models.CharField(max_length=63)
    created = models.DateTimeField(auto_now_add=True)
    
    status = models.IntegerField(choices=UserStatus, default=UserStatus.ACTIVE)
    last_seen = models.TimeField(auto_now_add=True)
    # pic = models.ImageField()

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):  
        return self.phone

    def get_available_data(self):
        resp = dict()
        if self.username:
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
    
    def get_all_data(self):
        resp = dict()
        if self.username:
            resp['username'] = self.username
        if self.email:
            resp['email'] = self.email
            resp['is_shown_email'] = self.is_shown_email
        resp['name'] = self.name
        if self.phone:
            resp['phone'] = self.phone
            resp['is_shown_phone'] = self.is_shown_phone
        resp['description'] = self.description
        resp['status'] = self.status
        resp['created'] = self.created
        resp['id'] = self.id
        return resp

