# Generated by Django 4.2.3 on 2023-08-17 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailsender', '0015_remove_customer_mailing_list_mailing_customers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='customers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsender.customer'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='messages',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsender.mailtext'),
        ),
        migrations.AlterField(
            model_name='mailtext',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]