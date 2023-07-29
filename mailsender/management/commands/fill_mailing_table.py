import json

from django.core.management import BaseCommand

from mailsender.models import Mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('fixtures/mailing.json') as file:
            mailing = json.load(file)

        mailings_for_create = []

        for model in mailing:
            mailings_for_create.append(Mailing(pk=model['pk'],
                                               mailing_datetime=model['fields']['mailing_datetime'],
                                               once=model['fields']['once'],
                                               every_week=model['fields']['every_week'],
                                               every_month=model['fields']['every_month'],
                                               status=model['fields']['status']))

        Mailing.objects.all().delete()
        Mailing.objects.bulk_create(mailings_for_create)
