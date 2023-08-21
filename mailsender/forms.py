from django import forms
from mailsender.models import Mailing, MailText, Customer


class MailingForm(forms.ModelForm):
    """
    Форма для модели Mailing
    """
    class Meta:
        model = Mailing
        fields = ('mailing_datetime', 'status', 'customers', 'every_day', 'every_week', 'every_month')
        widgets = {
            'mailing_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MailTextForm(forms.ModelForm):
    """
    Форма для модели MailText
    """
    class Meta:
        model = MailText
        fields = ['topic', 'message']


class CustomerCreateForm(forms.ModelForm):
    """
    Класс формы клиента для вьюхи CustomersCreateView
    """

    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'middle_name', 'email']
