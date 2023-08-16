from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from mailsender.forms import MailTextForm, MailingForm, CustomerForm
from mailsender.models import MailText
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


class MailingManagementCreateView(View):
    template_name = 'mailsender/mailing_form.html'

    def get(self, request):
        mailing_form = MailingForm()
        mail_text_form = MailTextForm()
        customer_form = CustomerForm()
        return render(request, self.template_name,
                      {'mailing_form': mailing_form, 'mail_text_form': mail_text_form, 'customer_form': customer_form})

    def post(self, request):
        mailing_option = request.POST.get('mailing_option')
        mailing_datetime = request.POST.get('mailing_datetime')

        mailing_form = MailingForm(request.POST)
        mail_text_form = MailTextForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if mailing_form.is_valid() and mail_text_form.is_valid() and customer_form.is_valid():
            mailing_instance = mailing_form.save(commit=False)
            mailing_instance.creator = request.user
            mailing_instance.mailing_datetime = datetime.strptime(mailing_datetime, '%Y-%m-%dT%H:%M')

            if mailing_option == 'once':
                mailing_instance.once = True
                mailing_instance.every_week = False
                mailing_instance.every_month = False
            elif mailing_option == 'every_week':
                mailing_instance.once = False
                mailing_instance.every_week = True
                mailing_instance.every_month = False
            elif mailing_option == 'every_month':
                mailing_instance.once = False
                mailing_instance.every_week = False
                mailing_instance.every_month = True

            mailing_instance.save()

            selected_customer = customer_form.cleaned_data['existing_customer']
            if selected_customer:
                selected_customer.mailing_list = mailing_instance
                selected_customer.save()

            mail_text_instance = mail_text_form.save(commit=False)
            mail_text_instance.mailing = mailing_instance
            mail_text_instance.save()

            return redirect('mailsender:home')

        return render(request, self.template_name,
                      {'mailing_form': mailing_form, 'mail_text_form': mail_text_form, 'customer_form': customer_form})


class MailingDeleteView(DeleteView):
    model = MailText
    template_name = 'mailsender/mailing_delete.html'
    success_url = reverse_lazy('mailsender:home')
