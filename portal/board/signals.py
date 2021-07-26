# from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.urls import reverse

from .models import Reply
from .tasks import send_mail


@receiver(post_save, sender=Reply)
def on_reply_send_mail(sender, instance, created, update_fields, **kwargs):
    if created:
        site = 'https://{domain}'.format(
            domain=Site.objects.get_current().domain,
        )

        url = '{domain}{path}'.format(
            domain=site,
            path=reverse('reply_list_view', urlconf='board.urls'),
        )

        html_content = render_to_string(
            'email/mail_reply.html',
            {
                'reply': instance,
                'site': site,
                'url': url,
            }
        )
        txt_content = render_to_string(
            'email/mail_reply.txt',
            {
                'reply': instance,
                'site': site,
                'url': url,
            }
        )
        subject = render_to_string(
            'email/subject_reply.txt',
            {
                'site': site,
            }
        )
        mail_to = instance.ad_id.user_id.email

        send_mail.delay(mail_to, subject, txt_content, html_content)

    else:
        print(update_fields)
        if {'is_approved': True} in update_fields:
            pass
