from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import *
from .views import *
from django.core.signals import request_finished


@receiver(post_save, sender=Client, dispatch_uid='example_method')
def send_user_activation_email(sender, instance, **kwargs):
    persons_send_activation_email(instance.id)


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
