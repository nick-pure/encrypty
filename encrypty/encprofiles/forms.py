from django.forms import ModelForm
from django import forms
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'description', 'username', 'phone', 'email', 'is_hidden_phone', 'password', 'is_hidden_email']

    def clean_username(self):
        username = self.cleaned_data['username']
        for char in username:
            if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890':
                raise forms.ValidationError('Invalid characters are used')
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        for char in password:
            if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890!@#$%^&*():;\'\"/\\?><~':
                raise forms.ValidationError('Invalid characters are used')
        if len(password) < 8:
            raise forms.ValidationError('Password is too short')
        return password
    

