from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirmation/', TemplateView.as_view(template_name='users/email_confirmation_sent.html'),
         name='email_confirmation'),
    path('verify/<int:rand_key>/', VerifyEmailView.as_view(), name='verify_email'),
    path('email-confirmed/', TemplateView.as_view(template_name='users/email_confirmed.html'), name='email_confirmed'),
    path('email-confirmation-failed/', TemplateView.as_view(template_name='users/email_confirmation_failed.html')),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-done/', TemplateView.as_view(template_name='users/reset_password_done.html'),
         name='reset_password_done'),
    path('reset-password-failed/', TemplateView.as_view(template_name='users/reset_password_failed.html'),
         name='reset_password_failed')
]
