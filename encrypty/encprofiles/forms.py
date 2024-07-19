from django.forms import ModelForm
from django import forms
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'description', 'username', 'phone', 'email', 'is_shown_phone', 'password', 'is_shown_email']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number is invalid")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number is taken")
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        for char in username:
            if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890':
                raise forms.ValidationError('Invalid characters are used')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        for char in password:
            if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890!@#$%^&*():;\'\"/\\?><~':
                raise forms.ValidationError('Invalid characters are used')
        if len(password) < 8:
            raise forms.ValidationError('Password is too short')
        return password
    

