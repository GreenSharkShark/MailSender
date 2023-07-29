from django.urls import path

from mailsender.apps import MailsenderConfig
from mailsender.views import *

app_name = MailsenderConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
]
