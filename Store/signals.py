from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


'''
The sender is user while the receiver is shipping_details and kyc
The receiver decorator gets what type of signal to receive and from whom(sender)
The build_shipping_details and kyc function checks if our signal is true( if created == True) and then does a task which is to create a shipping_details and kyc for that user
The save_shipping_details and kyc simply saves our shipping_details and kyc. Observe that the created parameter is absent

Last task is to go under apps.py module under Storeconfig class and add a function to import signals module:
    def ready(self):
        import Store.signals 
'''


@receiver(post_save, sender=User)
def build_kyc(sender, instance, created, **kwargs):
    if created:
        KYC.objects.create(user=instance)

@receiver(post_save, sender=User)       
def save_kyc(sender, instance, **kwargs):
    instance.kyc.save()

@receiver(post_save, sender=User)
def build_shippingdetail(sender, instance, created, **kwargs):
    if created:
        ShippingDetail.objects.create(user=instance)

@receiver(post_save, sender=User)       
def save_shippingdetail(sender, instance, **kwargs):
    instance.shippingdetail.save()
