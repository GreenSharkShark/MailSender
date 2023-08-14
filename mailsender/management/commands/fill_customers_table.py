import json

from django.core.management import BaseCommand
from mailsender.models import Customer, Mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('fixtures/customers.json', encoding='utf-8') as file:
            customers = json.load(file)

        customers_for_create = []

        for model in customers:
            mailing_list_id = model['fields']['mailing_list']
            mailing_list_instance = Mailing.objects.get(pk=mailing_list_id) if mailing_list_id else None

            customers_for_create.append(Customer(
                pk=model['pk'],
                mailing_list=mailing_list_instance,
                email=model['fields']['email'],
                first_name=model['fields']['first_name'],
                last_name=model['fields']['last_name'],
                middle_name=model['fields']['middle_name'],
            ))

        Customer.objects.all().delete()
        Customer.objects.bulk_create(customers_for_create)
