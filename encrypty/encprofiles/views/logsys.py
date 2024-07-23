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
@single_way_check('name', 'phone', 'password')
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return Data({'phone': form['phone'].value(), 'password' : form['password'].value()}, 200)
        else:
            return Er(form.errors, 400)
    return Er('Invalid HTTP method', 405)

@csrf_exempt
@single_way_check('phone', 'password')
def user_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        phone = form['phone'].value()
        password = form['password'].value()
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return Ok('Login successful', 200)
        else:
            return Er('Invalid phone or password', 405)
    return Er('Invalid HTTP method', 405)

@csrf_exempt
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Ok('Logout successful', 200)
    return Er('Invalid HTTP method', 405)
