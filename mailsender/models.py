from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """
    Рассылка (настройки):
        время рассылки;
        периодичность: раз в день, раз в неделю, раз в месяц;
        статус рассылки: завершена, создана, запущена.
    """
    mailing_datetime = models.DateTimeField(verbose_name='Время и дата рассылки')
    once = models.BooleanField(default=True, verbose_name='Единоразовая рассылка')
    every_week = models.BooleanField(default=False, verbose_name='Рассылка раз в неделю')
    every_month = models.BooleanField(default=False, verbose_name='Рассылка раз в месяц')
    status = models.BooleanField(default=True, verbose_name='Активировать рассылку')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)


class Customer(models.Model):
    """
    Клиент сервиса:
        контактный email,
        ФИО,
        комментарий.
    """
    mailing_list = models.ForeignKey('Mailing', on_delete=models.SET_NULL, **NULLABLE)
    email = models.EmailField(max_length=254, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Отчество')

    def __str__(self):
        return f'{self.first_name}'


class MailText(models.Model):
    """
    Сообщение для рассылки:
        тема письма,
        тело письма.
    """
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, default=None)
    topic = models.CharField(max_length=100, verbose_name='Тема рассылки')
    message = models.TextField(verbose_name='Текст сообщения')


class Logs(models.Model):
    """
    Логи рассылки:
        дата и время последней попытки;
        статус попытки;
        ответ почтового сервера, если он был.
    """
    mailing_id = models.OneToOneField('Mailing', on_delete=models.CASCADE, default=None)
    datetime_of_last_mailing = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней рассылки')
    status = models.BooleanField(default=False, verbose_name='Статус рассылки')
