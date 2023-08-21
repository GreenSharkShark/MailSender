from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Post
from config import settings
from mailsender.forms import MailTextForm, CustomerCreateForm, MailingForm
from mailsender.models import Customer, Mailing, Logs
from django.urls import reverse_lazy


class DispatchMixin:
    """
    Класс, который запрещает доступ к объектам, создателями которых не является текущий пользователь
    """
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.creator != self.request.user:
            return HttpResponseForbidden(
                "У вас нет прав на редактирование или удаление продукта, создателем которого вы не являетесь."
            )
        return super().dispatch(request, *args, **kwargs)


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.path
        return context


class HomeListView(LoginRequiredMixin, ContextMixin, ListView):
    """
    Класс для отображения главной страницы сайта. В класс передаются сразу две модели:
    MailText и Post из приложения Blog
    """
    model = Mailing
    template_name = 'mailsender/home.html'

    def get_context_data(self, **kwargs):
        """
        В этом методе в контекст добавляются 3 случайных объекта модели Post
        """
        context = super().get_context_data(**kwargs)
        random_posts = sample(list(Post.objects.all()), 3)

        context['post_objects'] = random_posts

        return context


class MailingManagementListView(LoginRequiredMixin, ContextMixin, ListView):
    model = Mailing
    template_name = 'mailsender/mailing_management_list.html'


class MailingManagementDetailView(LoginRequiredMixin, ContextMixin, DispatchMixin, DetailView):
    model = Mailing
    template_name = 'mailsender/mailing_management_detail.html'


class MailingManagementUpdateView(LoginRequiredMixin, ContextMixin, DispatchMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailsender/mailing_management_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm(instance=self.object)
        context['mailtext_form'] = MailTextForm(instance=self.object.messages)
        return context

    def form_valid(self, form):
        mailing_form = MailingForm(self.request.POST, instance=self.object)
        mailtext_form = MailTextForm(self.request.POST, instance=self.object.messages)

        if mailing_form.is_valid() and mailtext_form.is_valid():
            mailing = mailing_form.save(commit=False)
            periodicity = self.request.POST.get('periodicity')
            if periodicity == 'every_day':
                mailing.every_day = True
                mailing.every_week = False
                mailing.every_month = False
            elif periodicity == 'every_week':
                mailing.every_day = False
                mailing.every_week = True
                mailing.every_month = False
            elif periodicity == 'every_month':
                mailing.every_day = False
                mailing.every_week = False
                mailing.every_month = True
            mailtext_form.save()
            mailing.save()
            return super().form_valid(form)
        else:
            return render(self.request, self.template_name,
                          {'mailing_form': mailing_form, 'mailtext_form': mailtext_form})

    def get_success_url(self):
        return reverse_lazy('mailsender:mailing_management_detail', kwargs={'pk': self.object.pk})


class MailingManagementCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания рассылки.
    """

    model = Mailing
    form_class = MailingForm
    template_name = 'mailsender/mailing_create.html'

    # Здесь передаем в контекст две формы для заполнения
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm
        context['mailtext_form'] = MailTextForm
        return context

    def form_valid(self, form):
        mail_text_form = MailTextForm(self.request.POST)

        mailing = form.save(commit=False)
        mail_text = mail_text_form.save(commit=False)

        mail_text.creator = self.request.user
        mail_text.save()

        mailing.messages = mail_text
        mailing.creator = self.request.user
        periodicity = self.request.POST.get('periodicity')
        if periodicity == 'every_day':
            mailing.every_day = True
        elif periodicity == 'every_week':
            mailing.every_week = True
        else:
            mailing.every_month = True

        logs = Logs.objects.create()
        mailing.logs = logs

        mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailsender:mailing_management_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(LoginRequiredMixin, DispatchMixin, DeleteView):
    """
    Класс для удаления рассылки
    """
    model = Mailing
    template_name = 'mailsender/mailing_delete.html'
    success_url = reverse_lazy('mailsender:home')


class CustomersListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'mailsender/customers_list_view.html'


class CustomersCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'mailsender/customers_create_view.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('mailsender:customers_list')

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.creator = self.request.user
        customer.save()
        return super().form_valid(form)


class CustomersUpdateView(LoginRequiredMixin, DispatchMixin, UpdateView):
    model = Customer
    template_name = 'mailsender/customers_update_view.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('mailsender:customers_list')


class CustomersDeleteView(LoginRequiredMixin, DispatchMixin, DeleteView):
    model = Customer
    template_name = 'mailsender/customer_delete.html'
    success_url = reverse_lazy('mailsender:customers_list')
