# Generated by Django 4.2.3 on 2023-08-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0026_alter_logs_datetime_of_last_mailing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='status',
            field=models.BooleanField(blank=True, null=True, verbose_name='Статус рассылки'),
        ),
    ]
