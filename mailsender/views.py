from django.views.generic import ListView, DetailView, UpdateView
from mailsender.models import MailText, Mailing
from django.urls import reverse_lazy
from datetime import datetime


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.path
        return context


class HomeListView(ContextMixin, ListView):
    model = MailText
    template_name = 'mailsender/home.html'

    def get_queryset(self):
        return super().get_queryset().filter(mailing__status=True)


class MailingManagementListView(ContextMixin, ListView):
    model = MailText
    template_name = 'mailsender/mailing_management_list.html'

    def get_queryset(self):
        return super().get_queryset().all()


class MailingManagementDetailView(ContextMixin, DetailView):
    model = MailText
    template_name = 'mailsender/mailing_management_detail.html'


class MailingManagementUpdateView(ContextMixin, UpdateView):
    model = MailText
    template_name = 'mailsender/mailing_management_update.html'
    fields = ('topic', 'message',)

    def get_success_url(self):
        return reverse_lazy('mailsender:mailing_management_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        periodicity = self.request.POST.get('periodicity')
        status = self.request.POST.get('status')

        if periodicity == 'monthly' or periodicity == 'weekly':
            date = self.request.POST.get('date')
            self.object.mailing.mailing_datetime = date
        else:
            self.object.mailing.mailing_datetime = datetime.today()

        self.object.mailing.once = periodicity == 'daily'
        self.object.mailing.every_week = periodicity == 'weekly'
        self.object.mailing.every_month = periodicity == 'monthly'
        self.object.mailing.status = status == 'active'
        self.object.mailing.save()
        return super().form_valid(form)
