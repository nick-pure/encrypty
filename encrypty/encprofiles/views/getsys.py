from encprofiles.forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from encprofiles.models import User
from django.contrib.auth import authenticate, login, logout
from encprofiles.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .checker import single_way_check, few_ways_checker
from .responses import Ok, Er, Data

class Searcher:
    def get_user(self, arg, user_searcher_arg):
        key, value = list(arg.items())[0]
        if len(value) == 0:
            return {}
        try:
            data = eval(f"User.objects.get({key}=value)")
            if key == 'phone' or key == 'email':
                if not eval(f"data.is_shown_{key}"):
                    return {}
            if eval(f"data.{key}") == user_searcher_arg:
                return {}
            return data.get_available_data()
        except User.DoesNotExist:
            return {}
    def get_users(self, arg, user_searcher_args):
        users = list()
        if len(arg) == 0:
            return {}
        for field in ['name', 'description', 'username', 'phone', 'email']:
            if field in ("phone", "email"):
                for value in eval(f"User.objects.filter({field}__contains=arg).filter(is_shown_{field}=True)"):
                    if eval(f"data.{field}") != eval(f"user_searcher_args.{field}"):
                        users.append(value.get_available_data())
            else:
                for value in eval(f"User.objects.filter({field}__contains=arg)"):
                    if not (field == 'username' and eval(f"data.{field}") == user_searcher_args.username):
                        users.append(value.get_available_data())

        users = list({v['id'] : v for v in users}.values())
        return users

searcher = Searcher()

@login_required
def get_by_(request, field):
    if request.method == 'GET':
        if field not in ['id', 'username', 'phone', 'email']:
            return Er('Invalid field', 405) 
        return Data({'user' : searcher.get_user({field: request.GET['arg']}, eval(f"request.user.{field}"))}, 200)
    else:
        return Er('Invalid HTTP method', 405)
    
@login_required
def get(request):   
    if request.method == 'GET':
        return Data({'users' : searcher.get_users(request.GET['arg'], request.user)}, status=200)
    else:
        return Er('Invalid HTTP method', 405)

@login_required
def get_my_profile(request):
    if request.method == 'GET':
        return Er('Invalid HTTP method', 405)