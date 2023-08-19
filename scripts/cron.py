import os
import django
from django.core.mail import send_mail
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# если я импортирую модель в начале файла, до django.setup(), то все перестает работать и я не знаю почему
from mailsender.models import Mailing


def save_date_of_last_mail_sending(mailing_object: Mailing, current_datetime: datetime):
    """
    Функция для сохранения в объект модели даты и времени последней рассылки
    """
    mailing_object.date_of_last_sending = current_datetime
    mailing_object.save()


def get_data_from_mailing_model():
    mailing_object = Mailing.objects.filter(status=True)

    for mailing in mailing_object:

        datetime_to_send = mailing.mailing_datetime
        last_sending_date = mailing.date_of_last_sending
        current_datetime = datetime.now()

        # аргументы передаваемые в функцию send_mail()
        mailing_args = [
            mailing.messages.topic,
            mailing.messages.message,
            'test',
            [mailing.customers.email]
        ]

        # обработка отправки ежедневных рассылок

        if mailing.every_day:

            # если в базе уже записана дата последней отправки, то вычисляем разницу между текущим временем
            # и временем последней отправки, если дельта больше суток, то отправляем письмо

            if last_sending_date and (current_datetime - last_sending_date) >= timedelta(days=1):
                send_mail(*mailing_args, fail_silently=False)

                # обновляем дату последней отправки
                save_date_of_last_mail_sending(mailing, current_datetime)

            # если в базе нет даты последней отправки, значит отправка еще ни разу не производилась,
            # а значит проверяем время отправки и если текущее время больше либо равно времени отправки,
            # значит отправляем письмо

            elif not last_sending_date and current_datetime.time() > datetime_to_send.time():
                send_mail(*mailing_args, fail_silently=False)

                # обновляем дату последней отправки
                save_date_of_last_mail_sending(mailing, current_datetime)

        #  обработка отправки еженедельных рассылок

        elif mailing.every_week:
            # если день недели = дню недели который задан для отправки и текущее время
            # больше времени отправки - отправляем письмо
            if datetime_to_send.weekday() == current_datetime.weekday() and current_datetime.time() > datetime_to_send.time():
                send_mail(*mailing_args, fail_silently=False)

                # обновляем дату последней отправки(здесь это не обязательно,
                # так как дата последней рассылки в данном случае не важна, но мне просто так хочется)
                save_date_of_last_mail_sending(mailing, current_datetime)

        #  обработка отправки ежемесячных рассылок

        elif mailing.every_month:

            # при ежемесячной рассылке просто сравниваем день отправки с текущим днем
            # если дата отправки будет задана, например, 31 числа, а в текущем месяце дней меньше,
            # то рассылка будет совершена в ближайшем месяце, в котором есть 31 день.

            if datetime_to_send.day == current_datetime.day:
                send_mail(*mailing_args, fail_silently=False)

                # обновляем дату последней отправки
                save_date_of_last_mail_sending(mailing, current_datetime)


if '__name__' == '__main__':
    get_data_from_mailing_model()
