from django.shortcuts import render
from encprofiles import models
from .forms import UserForm
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.save()
            return JsonResponse({'status':'ok', 'data':{'username':data.username, 'password':data.password}})
        else:
            return JsonResponse({'status':'wrong', 'data':{'description':form.errors}})
    else:
        return JsonResponse({'status':'wrong', 'data':{'description':'GET request is not supported'}})
    
@csrf_exempt
def get_by_username(request, username):
    if request.method == 'GET':
        try:
            data = User.objects.get(username=username)
            return JsonResponse({'status':'ok', 'data': data.get_all_data()})
        except User.DoesNotExist:
            return JsonResponse({'status':'ok', 'data':{'description':'User doesn\'t exist'}})
    else:
        return JsonResponse({'status':'wrong', 'data':{'description':'GET request is not supported'}})
    
@csrf_exempt
def get_by_phone(request, phone):
    if request.method == 'GET':
        try:
            data = User.objects.get(phone=phone)
            if data.is_hidden_phone:
                raise User.DoesNotExist()
            return JsonResponse({'status':'ok', 'data': data.get_all_data()})
        except User.DoesNotExist:
            return JsonResponse({'status':'ok', 'data':{'description':'User doesn\'t exist'}})
    else:
        return JsonResponse({'status':'wrong', 'data':{'description':'GET request is not supported'}})  

@csrf_exempt
def get_by_email(request, email):
    if request.method == 'GET':
        try:
            data = User.objects.get(email=email)
            if data.is_hidden_email:
                raise User.DoesNotExist()
            return JsonResponse({'status':'ok', 'data': data.get_all_data()})
        except User.DoesNotExist:
            return JsonResponse({'status':'ok', 'data':{'description':'User doesn\'t exist'}})
    else:
        return JsonResponse({'status':'wrong', 'data':{'description':'GET request is not supported'}})  