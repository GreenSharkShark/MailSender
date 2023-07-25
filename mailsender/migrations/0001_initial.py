# Generated by Django 4.2.3 on 2023-07-25 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_last_mailing', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней рассылки')),
                ('status', models.BooleanField(default=False, verbose_name='Статус рассылки')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.TimeField(auto_now_add=True, verbose_name='Время рассылки')),
                ('once', models.BooleanField(default=True, verbose_name='Единоразовая рассылка')),
                ('every_week', models.BooleanField(default=False, verbose_name='Рассылка раз в неделю')),
                ('every_month', models.BooleanField(default=False, verbose_name='Рассылка раз в месяц')),
                ('status', models.CharField(max_length=50, verbose_name='Статус рассылки')),
            ],
        ),
        migrations.CreateModel(
            name='MailText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='Тема рассылки')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
            ],
        ),
    ]
