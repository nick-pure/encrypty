from encprofiles.forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from encprofiles.models import User
from django.contrib.auth import authenticate, login, logout
from encprofiles.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

class Editor:
    def edit_user(self, user, field, new_value):
        user = User.objects.get(id=user)
        if eval(f"user.{field}") == new_value:
            return
        if field in ['username', 'email']:
            try:
                eval(f"User.objects.get({field}=new_value)")
                raise ValueError("Field is already used")
            except User.DoesNotExist:
                eval(f"user.{field} = new_value")
                user.save()
        else:
            eval(f"user.{field} = new_value")
            user.save()

editor = Editor()

@login_required
def edit_profile(request, field):
    if request.method == 'POST':
        if field not in ['name', 'description', 'username', 'email', 'is_shown_phone', 'is_shown_email']:
            return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid field'}}, status=401)
        try:
            
            editor.edit_user(request.user.id, field, request.POST['new_value'])
            return JsonResponse({'status': 'ok', 'info': {'description': f"Profile is successfuly edited"}}, status=403)
        except ValueError as e:
            return JsonResponse({'status': 'wrong', 'info': {'description': f"{e}"}}, status=403)
    else:
        return JsonResponse({'status': 'wrong', 'info': {'description': 'Invalid HTTP method'}}, status=405)