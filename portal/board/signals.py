from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Reply


# @receiver(post_save, sender=Reply)
# def on_reply_send_mail(sender, instance, created, **kwargs):
#     if created:
#         reply_data = {
#             'user': instance.ad_id.user_id,
#             'ad_header': instance.ad_id.header
#             ''
#         }


#     if action == 'post_add':
#         category_lst = list(sender.objects.filter(post=instance.id).
#                             values('category'))
#         for category in category_lst:
#             mailing_list = list(Mailing.objects.filter(
#                 category=category['category']).values('subscribers__username',
#                                                       'subscribers__email'))
#             for mail in mailing_list:

#                 send_mail.delay(instance.id, mail)
