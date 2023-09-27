from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = config("ADMIN_NAME")
        if not len(User.objects.all().filter(username=username)):
            password = config("ADMIN_PASS")
            print(f'Conta do usuário {username} será criada!')
            admin = User.objects.create_superuser(
                username=username, password=password)
            admin.is_active = True
            admin.is_staff = True
            admin.save()
        else:
            print('Conta de administrador já existe!')
