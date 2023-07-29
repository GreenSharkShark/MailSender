from django.views.generic import ListView
from mailsender.models import MailText, Mailing


class HomeListView(ListView):
    model = MailText
    template_name = 'mailsender/home.html'

    def get_queryset(self):
        return super().get_queryset().filter(mailing__status=True)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['mail_objects'] = MailText.objects.select_related('mailing').all()
    #     return context
