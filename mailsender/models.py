from django.db import models

NULLABLE = {'blank': True, 'null': True}


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


class Mailing(models.Model):
    """
    Рассылка (настройки):
        время рассылки;
        периодичность: раз в день, раз в неделю, раз в месяц;
        статус рассылки: завершена, создана, запущена.
    """
    mailing_time = models.TimeField(auto_now_add=True, verbose_name='Время рассылки')
    once = models.BooleanField(default=True, verbose_name='Единоразовая рассылка')
    every_week = models.BooleanField(default=False, verbose_name='Рассылка раз в неделю')
    every_month = models.BooleanField(default=False, verbose_name='Рассылка раз в месяц')
    status = models.CharField(max_length=50, verbose_name='Статус рассылки')


class MailText(models.Model):
    """
    Сообщение для рассылки:
        тема письма,
        тело письма.
    """
    topic = models.CharField(max_length=100, verbose_name='Тема рассылки')
    message = models.TextField(verbose_name='Текст сообщения')


class Logs(models.Model):
    """
    Логи рассылки:
        дата и время последней попытки;
        статус попытки;
        ответ почтового сервера, если он был.
    """
    datetime_of_last_mailing = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней рассылки')
    status = models.BooleanField(default=False, verbose_name='Статус рассылки')
