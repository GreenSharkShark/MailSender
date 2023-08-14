import json

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='zhorik@zeniuk.by',
            first_name='Zhorik',
            last_name='Zeniuk',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('123g123ofuck')
        user.save()
