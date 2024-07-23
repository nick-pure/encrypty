from encprofiles.forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from encprofiles.models import User
from django.contrib.auth import authenticate, login, logout
from encprofiles.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .checker import single_way_check, few_ways_checker
class Editor:
    @classmethod
    def edit_user(self, user, field, new_value):
        if eval(f"user.{field} == new_value"):
            return
        if field == 'name' and not new_value:
            raise ValueError('Name can\'t be nothing')
        if field == 'email' or field == 'username':
            try:
                eval(f"User.objects.get({field}=new_value)")
                raise ValueError(f'{str(field).capitalize()} already exists')
            except User.DoesNotExist:
                setattr(user, field, new_value)
                user.save()
        if new_value == "True":
            new_value = True
        elif new_value == "False":
            new_value = False
        setattr(user, field, new_value)
        user.save()


@login_required
@single_way_check('new_value')
def edit_profile(request, field):
    if request.method == 'POST':
        if field not in ['name', 'description', 'username', 'email', 'is_shown_phone', 'is_shown_email']:
            return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid field'}}, status=401)
        try:
            Editor.edit_user(request.user, field, request.POST['new_value'])
            return JsonResponse({'status': 'ok', 'info': {'description': f"Profile is successfuly edited"}}, status=200)
        except ValueError as e:
            return JsonResponse({'status': 'wrong', 'info': {'description': f"{e}"}}, status=403)
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)