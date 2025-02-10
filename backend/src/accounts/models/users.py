from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        if self.get_full_name():
            return f'{self.get_full_name()} ({self.username})'
        return self.username
