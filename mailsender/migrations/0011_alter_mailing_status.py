# Generated by Django 4.2.3 on 2023-08-15 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0010_alter_mailing_mailing_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Активировать рассылку'),
        ),
    ]
