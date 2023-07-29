from django.urls import path

from mailsender.apps import MailsenderConfig
from mailsender.views import *

app_name = MailsenderConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('mailing-management/', MailingManagementListView.as_view(), name='mailing_management'),
    path('mailing-management/<int:pk>/', MailingManagementDetailView.as_view(), name='mailing_management_detail'),
    path('mailing-management-update/<int:pk>/', MailingManagementUpdateView.as_view(), name='mailing_management_update')
]
