from encprofiles.forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from encprofiles.models import User
from django.contrib.auth import authenticate, login, logout
from encprofiles.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .checker import *
from .responses import *
from django.contrib.auth.models import AnonymousUser
from django.middleware.csrf import get_token

@csrf_exempt
def check_auth(request):
    if not isinstance(request.user, AnonymousUser):
        return Data({'isAuthenticated': True}, 200)
    return Data({'isAuthenticated': False}, 400)



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
        err = str()
        for key, value in dict(form.errors).items():
            err = key + ': ' + value[0] + '; '
        return Er(err[:-2], 400)

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
        response = Ok('Login successful', 200)
        response.set_cookie('csrftoken', get_token(request))
        return response
    else:
        return Er('Invalid phone or password', 405)

@csrf_exempt
@method_checker('POST')
@login_required
def user_logout(request):
    logout(request)
    return Ok('Logout successful', 200)
