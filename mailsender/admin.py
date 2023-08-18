from django.contrib import admin

from mailsender.models import MailText, Customer, Mailing


@admin.register(MailText)
class MailtextAdmin(admin.ModelAdmin):
    list_display = ('topic',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email',)


@admin.register(Mailing)
class Administrator(admin.ModelAdmin):
    list_display = ('creator', 'status')

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Administrator').exists():
            return ['creator', 'mailing_datetime', 'once', 'every_week', 'every_month']
        return []

