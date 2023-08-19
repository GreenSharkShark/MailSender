# Generated by Django 4.2.3 on 2023-08-19 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0023_mailing_date_of_last_sending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logs',
            name='mailing_id',
        ),
        migrations.AddField(
            model_name='mailing',
            name='logs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailsender.logs'),
        ),
    ]
