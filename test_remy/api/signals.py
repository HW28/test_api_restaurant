from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import *
from .functions import *
from django.core.signals import request_finished


@receiver(post_save, sender=OrderTrack, dispatch_uid='update_order')
def order_track_notification(sender, instance, **kwargs):
    order_notification(instance)


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
