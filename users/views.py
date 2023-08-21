from random import randint

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView
from users.services import made_rand_key_for_verify_and_send_mail, reset_password_and_send_mail
from users.fomrs import UserRegisterForm, UserProfileForm, UserResetPasswordForm
from users.models import User
from django.http import HttpResponseRedirect


class RegisterView(CreateView):
    """
    Класс для регистрации пользователя на сайте
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:email_confirmation')

    def form_valid(self, form):
        made_rand_key_for_verify_and_send_mail(self, form)
        return super().form_valid(form)


class VerifyEmailView(View):
    """
    Класс для верификации почты пользователя
    """
    def get(self, request, rand_key):
        try:
            user = User.objects.get(rand_key=rand_key)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('users:email_confirmed'))
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('users:email_confirmation_failed'))


class ResetPasswordView(FormView):
    """
    Класс для сброса пароля на автоматически сгенерированный
    """
    model = User
    template_name = 'users/reset_password.html'
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('users:reset_password_done')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        reset_password_and_send_mail(username)
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailsender:home')

    def get_object(self, queryset=None):
        return self.request.user
