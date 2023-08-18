from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Post
from mailsender.forms import MailTextForm, MailingForm, CustomerForm, CustomerCreateForm, MailingTestForm
from mailsender.models import MailText, Customer, Mailing
from django.urls import reverse_lazy
from datetime import datetime


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

    def get_queryset(self):
        return super().get_queryset().all()


class MailingManagementDetailView(LoginRequiredMixin, ContextMixin, DispatchMixin, DetailView):
    model = Mailing
    template_name = 'mailsender/mailing_management_detail.html'


class MailingManagementUpdateView(LoginRequiredMixin, ContextMixin, DispatchMixin, UpdateView):
    model = Mailing
    form_class = MailingTestForm
    template_name = 'mailsender/mailing_management_update.html'

    def get_success_url(self):
        return reverse_lazy('mailsender:mailing_management_detail', kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #     periodicity = self.request.POST.get('periodicity')
    #     status = self.request.POST.get('status')
    #
    #     if periodicity == 'monthly' or periodicity == 'weekly':
    #         date = self.request.POST.get('date')
    #         self.object.mailing.mailing_datetime = date
    #     else:
    #         self.object.mailing.mailing_datetime = datetime.today()
    #
    #     self.object.mailing.once = periodicity == 'daily'
    #     self.object.mailing.every_week = periodicity == 'weekly'
    #     self.object.mailing.every_month = periodicity == 'monthly'
    #     self.object.mailing.status = status == 'active'
    #     self.object.mailing.save()
    #     return super().form_valid(form)


class MailingManagementCreateView(LoginRequiredMixin, View):
    """
    Класс для создания рассылки. В классе обрабатываются сразу три связанных между собой
    внешним ключом модели. Для каждой модели создана отдельная форма в forms.py.
    """
    template_name = 'mailsender/mailing_form.html'

    def get(self, request):
        mailing_form = MailingForm()
        mail_text_form = MailTextForm()
        customer_form = CustomerForm()
        return render(request, self.template_name,
                      {'mailing_form': mailing_form, 'mail_text_form': mail_text_form, 'customer_form': customer_form})

    def post(self, request):
        mailing_option = request.POST.get('mailing_option')  # получаем из шаблона периодичность рассылки
        mailing_datetime = request.POST.get('mailing_datetime')  # получаем из шаблона дату рассылки

        mailing_form = MailingForm(request.POST)
        mail_text_form = MailTextForm(request.POST)
        customer_form = CustomerForm(request.POST)

        # Обработка формы рассылки. Здесь в нее записывается дата, а так же периодичность рассылки
        if mailing_form.is_valid() and mail_text_form.is_valid() and customer_form.is_valid():

            # Получаем клиента для рассылки которого выбрал пользователь и сохраняем в его лист рассылок новую
            selected_customer = customer_form.cleaned_data['existing_customer']

            # Просто сохраняем объект модели с сообщением и темой рассылки
            mail_text_instance = mail_text_form.save(commit=False)
            mail_text_instance.creator = request.user
            mail_text_instance.save()

            mailing_instance = mailing_form.save(commit=False)
            mailing_instance.creator = request.user
            mailing_instance.mailing_datetime = datetime.strptime(mailing_datetime, '%Y-%m-%dT%H:%M')

            if mailing_option == 'every_week':
                mailing_instance.once = False
                mailing_instance.every_week = True
            elif mailing_option == 'every_month':
                mailing_instance.once = False
                mailing_instance.every_month = True

            mailing_instance.customers = selected_customer
            mailing_instance.messages = mail_text_instance
            mailing_instance.save()

            return redirect('mailsender:home')

        return render(request, self.template_name,
                      {'mailing_form': mailing_form, 'mail_text_form': mail_text_form, 'customer_form': customer_form})


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
