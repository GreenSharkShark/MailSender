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
    every_day = models.BooleanField(default=False, verbose_name='Ежедневная рассылка')
    every_week = models.BooleanField(default=False, verbose_name='Рассылка раз в неделю')
    every_month = models.BooleanField(default=False, verbose_name='Рассылка раз в месяц')
    status = models.BooleanField(default=True, verbose_name='Активировать рассылку')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    date_of_last_sending = models.DateTimeField(**NULLABLE, verbose_name='Время и дата последней рассылки')
    messages = models.ForeignKey('MailText', on_delete=models.CASCADE)
    customers = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    logs = models.ForeignKey('Logs', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'Рассылка {self.pk} от пользователя {self.creator}'


class Customer(models.Model):
    """
    Клиент сервиса:
        контактный email,
        ФИО,
        комментарий.
    """
    email = models.EmailField(max_length=254, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Отчество')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name}'


class MailText(models.Model):
    """
    Сообщение для рассылки:
        тема письма,
        тело письма.
    """
    topic = models.CharField(max_length=100, verbose_name='Тема рассылки')
    message = models.TextField(verbose_name='Текст сообщения')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Logs(models.Model):
    """
    Логи рассылки:
        дата и время последней попытки;
        статус попытки;
        ответ почтового сервера, если он был.
    """
    datetime_of_last_mailing = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней рассылки')
    status = models.BooleanField(default=False, verbose_name='Статус рассылки')
