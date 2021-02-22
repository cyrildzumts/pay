from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from payments.models import Balance


@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created,  **kwargs):
    if created:
        # first check if instance already has a account profile
        # if the user hasn't an associated account profile then we create an Profile account.
        #
        if not Balance.objects.filter(user=instance).exists():
            Balance.objects.create(user=instance, name=instance.get_full_name())
    return