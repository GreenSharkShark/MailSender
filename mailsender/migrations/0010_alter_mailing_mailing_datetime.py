# Generated by Django 4.2.3 on 2023-08-15 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0009_alter_mailing_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='mailing_datetime',
            field=models.DateTimeField(verbose_name='Время и дата рассылки'),
        ),
    ]
