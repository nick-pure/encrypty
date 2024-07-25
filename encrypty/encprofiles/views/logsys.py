from encprofiles.forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from encprofiles.models import User
from django.contrib.auth import authenticate, login, logout
from encprofiles.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .checker import *
from .responses import *

@csrf_exempt
def crya(request):
    return Ok('Hello!', 200)

@csrf_exempt
@method_checker('POST')
@single_way_check('name', 'phone', 'password')
def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return Data({'phone': form['phone'].value(), 'password' : form['password'].value()}, 200)
    else:
        return Er(form.errors, 400)

@csrf_exempt
@method_checker('POST')
@single_way_check('phone', 'password')
def user_login(request):
    form = UserForm(request.POST)
    phone = form['phone'].value()
    try:
        User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Er('User doesn\'t exist', 405)
    password = form['password'].value()
    user = authenticate(request, phone=phone, password=password)
    if user is not None:
        login(request, user)
        return Ok('Login successful', 200)
    else:
        return Er('Invalid phone or password', 405)

@csrf_exempt
@method_checker('POST')
@login_required
def user_logout(request):
    logout(request)
    return Ok('Logout successful', 200)
