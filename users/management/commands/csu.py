from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Класс для создания суперпользователя. Данные заполните сами
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='',
            first_name='',
            last_name='',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('')
        user.save()
