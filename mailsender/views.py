from django.views.generic import ListView, DetailView, UpdateView
from mailsender.models import MailText, Mailing
from django.urls import reverse_lazy


class HomeListView(ListView):
    model = MailText
    template_name = 'mailsender/home.html'

    def get_queryset(self):
        return super().get_queryset().filter(mailing__status=True)


class MailingManagementListView(ListView):
    model = MailText
    template_name = 'mailsender/mailing_management_list.html'

    def get_queryset(self):
        return super().get_queryset().all()


class MailingManagementDetailView(DetailView):
    model = MailText
    template_name = 'mailsender/mailing_management_detail.html'


class MailingManagementUpdateView(UpdateView):
    model = MailText
    template_name = 'mailsender/mailing_management_update.html'
    fields = ('topic', 'message',)
    success_url = reverse_lazy('mailing_management_detail')
