from .forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth import authenticate, login, logout
from .decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return JsonResponse({'status': 'ok', 'data': {'phone': form['phone'], 'password' : form['password']}}, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({'status': 'wrong', 'info': {'error': 'Invalid HTTP method'}}, status=405)

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

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'ok', 'info': {'description': 'Logout successful'}}, status=200)
    return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)


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
            if field in ("phone", "email"):
                for value in eval(f"User.objects.filter({field}__contains=arg).filter(is_shown_{field}=True)"):
                    users.append(value.get_all_data())
            else:
                for value in eval(f"User.objects.filter({field}__contains=arg)"):
                    users.append(value.get_all_data())

        users = list({v['id'] : v for v in users}.values())
        return users


searcher = Searcher()

@login_required
def get_by_username(request, username):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_user({"username": username})})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)

@login_required
def get_by_phone(request, phone):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_user({"phone": phone})})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)

@login_required
def get_by_id(request, id):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_user({"id": id})})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)
@login_required
def get(request, arg):
    if request.method == 'GET':
        return JsonResponse({'status' : 'ok', 'user' : searcher.get_users(arg)})
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)

@login_required
def get_user_phone(request):
    user = request.user
    return JsonResponse({"phone": user.phone})
