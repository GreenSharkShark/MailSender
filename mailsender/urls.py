from django.urls import path
from django.views.decorators.cache import cache_page
from mailsender.apps import MailsenderConfig
from mailsender.views import *

app_name = MailsenderConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('mailing-management/', MailingManagementListView.as_view(), name='mailing_management'),
    path('mailing-management/<int:pk>/', MailingManagementDetailView.as_view(), name='mailing_management_detail'),
    path('mailing-management-update/<int:pk>/', MailingManagementUpdateView.as_view(), name='mailing_update'),
    path('mailing-management-create/', cache_page(60)(MailingManagementCreateView.as_view()), name='mailing_management_create'),
    path('mailing-delete/<int:pk>/', cache_page(60)(MailingDeleteView.as_view()), name='mailing_delete'),
    path('customers-list/', CustomersListView.as_view(), name='customers_list'),
    path('customers-create/', cache_page(60)(CustomersCreateView.as_view()), name='customers_create'),
    path('customers-update/<int:pk>/', CustomersUpdateView.as_view(), name='customers_update'),
    path('customers-delete/<int:pk>/', cache_page(60)(CustomersDeleteView.as_view()), name='customers_delete'),
]
