from django.contrib import admin

from mailsender.models import MailText, Customer, Mailing


@admin.register(MailText)
class MailtextAdmin(admin.ModelAdmin):
    list_display = ('topic',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email',)


admin.site.register(Mailing)
