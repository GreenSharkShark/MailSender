# Generated by Django 4.2.3 on 2023-08-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0016_alter_customer_creator_alter_mailing_customers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='every_day',
            field=models.BooleanField(default=False, verbose_name='Единоразовая рассылка'),
        ),
    ]
