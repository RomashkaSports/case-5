from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as UserAdminDjango

from ..models import User


@register(User)
class UserAdmin(UserAdminDjango):
    pass
