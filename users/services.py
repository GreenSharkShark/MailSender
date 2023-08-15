from django.core.mail import send_mail
from django.shortcuts import redirect
from users.models import User
from random import randint
from django.urls import reverse


def reset_password_and_send_mail(username):
    try:
        user = User.objects.get(email=username)
        new_password = User.objects.make_random_password(length=12)
        user.set_password(new_password)
        user.save()
        send_mail(
            'Сброс пароля',
            f'Ваш новый пароль для входа: {new_password}',
            'test',
            [user.email],
            fail_silently=False
        )
    except User.DoesNotExist:
        return redirect('users:reset_password_failed')


def made_rand_key_for_verify_and_send_mail(self, form):
    """
    Функция для генерации случайного ключа для верификации и отправки сообщения со ссылкой для верификации на почту
    """
    user = form.save()
    user.rand_key = randint(1, 2147483644)
    user.save()
    verify_url = reverse('users:verify_email', args=[user.rand_key])
    verify_link = self.request.build_absolute_uri(verify_url)
    send_mail(
        'Подтвердите свой электронный адрес',
        f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: {verify_link}',
        'test',
        [user.email],
        fail_silently=False
    )
