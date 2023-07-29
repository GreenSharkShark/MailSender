import json

from django.core.management import BaseCommand

from mailsender.models import MailText, Mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('fixtures/mailtext.json') as file:
            mailtexts = json.load(file)

        mailtexts_for_create = []

        for model in mailtexts:
            mailing_id = model['fields']['mailing']
            mailing = Mailing.objects.get(pk=mailing_id)

            mailtexts_for_create.append(MailText(pk=model['pk'],
                                                 mailing_id=mailing.pk,
                                                 topic=model['fields']['topic'],
                                                 message=model['fields']['message']))

        MailText.objects.all().delete()
        MailText.objects.bulk_create(mailtexts_for_create)
