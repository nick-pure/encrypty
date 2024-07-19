from django.shortcuts import render
from encprofiles import models
from .forms import UserForm
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User


class Searcher:
    def get_user(self, arg):
        key, value = list(arg.items())[0]
        print(key, value)
        try:
            data = eval(f"User.objects.get({key}=value)")
            return data.get_all_data()
        except User.DoesNotExist:
            return {}
    def get_users(self, arg):
        users = list()
        for field in UserForm.Meta.fields:
            for value in eval(f"User.objects.filter({field}__contains=arg)"):
                users.append(value.get_all_data())

        users = list({v['id'] : v for v in users}.values())
        return users


searcher = Searcher()
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.save()
            return JsonResponse({'status': 'ok', 'data': {'username': data.username, 'password': data.password}})
        else:
            return JsonResponse({'status': 'wrong', 'data': {'description': form.errors}})
    else:
        return JsonResponse({'status': 'wrong', 'data': {'description': 'GET request is not supported'}})


@csrf_exempt
def get_by_username(request, username):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_user({"username": username})})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'GET request is not supported'}})


@csrf_exempt
def get_by_phone(request, phone):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_user({"phone": phone})})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'GET request is not supported'}})

@csrf_exempt
def get_by_id(request, id):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_user({"id": id})})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'GET request is not supported'}})

@csrf_exempt
def get(request, arg):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_users(arg)})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'GET request is not supported'}})