from django.contrib.auth import get_user_model

from django.dispatch import receiver
from django.db.models.signals import pre_save


@receiver(pre_save, sender=get_user_model())
def set_username(sender, instance, **kwargs):
    instance.username = instance.email
