# Generated by Django 4.2.3 on 2023-07-28 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0004_alter_logs_mailing_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='mailing_time',
        ),
        migrations.AddField(
            model_name='mailing',
            name='mailing_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время и дата рассылки'),
        ),
    ]
