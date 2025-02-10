from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from src.accounts.models import User
from src.utilities.text import filter_ascii


@csrf_exempt
def auth(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('ok')

        name = request.POST.get('name', '').strip()
        username = filter_ascii(request.POST.get('login', ''))
        password = request.POST.get('password', None)

        if name and username and password:
            user = User.objects.filter(username=username).exists()
            if not user:
                user = User.objects.create_user(
                    first_name=name,
                    username=username,
                )
                user.set_password(password)
                user.save()
                login(request, user)
                return HttpResponse('ok')
            else:
                return HttpResponse('Логин занят')
        else:
            user = authenticate(
                request=request,
                username=request.POST.get('login'),
                password=request.POST.get('password'),
            )
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponse('ok')
            return HttpResponse('Логин и пароль неверные')
    return HttpResponseNotAllowed(['POST'])

