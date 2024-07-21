from encprofiles.forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from encprofiles.models import User
from django.contrib.auth import authenticate, login, logout
from encprofiles.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return JsonResponse({'status': 'ok', 'data': {'phone': form['phone'].value(), 'password' : form['password'].value()}}, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid HTTP method'}}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        phone = form['phone'].value()
        password = form['password'].value()
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'ok', 'info': {'description': 'Login successful'}}, status=200)
        else:
            return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid phone or password'}}, status=405)
    return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid HTTP method'}}, status=405)

@csrf_exempt
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'ok', 'info': {'description': 'Logout successful'}}, status=200)
    return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)
