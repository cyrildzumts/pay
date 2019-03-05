from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Policy(models.Model):
    policy_id = models.IntegerField(blank=False)
    daily_limit = models.IntegerField(blank=False)
    weekly_limit = models.IntegerField(blank=False)
    monthly_limit = models.IntegerField(blank=False)
    commission = models.DecimalField()



class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    country = models.CharField(default='', max_length=50, blank=True)
    city = models.CharField(max_length=50)
    province = models.CharField(default='', max_length=50)
    address = models.CharField(default='', max_length=50)
    zip_code = models.CharField(default='', max_length=15)
    telefon = models.CharField(default='', max_length=15)
    newsletter = models.BooleanField(default=False)
    is_active_account = models.BooleanField(default=True)
    solde = models.IntegerField(default=0)
    created_at = models.DateField(auto_now=True)
    policy = models.ForeignKey(Policy, related_name="policy")


    class Meta:
        permissions = (
            ('deactivate_account', "Can deactivate a User"),
        )

    @models.permalink
    def get_absolute_url(self):
        return ('accounts:edit_user', (), {'pk': self.pk})


    
class IDCard(models.Model):
    card_number = models.IntegerField(blank=False)
    image = models.ImageField(blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)





def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        #user_profil = UserProfile(user=user)
        #user_profil.save()
        Account.objects.create(user=user)


@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    if hasattr(instance, 'account'):
        instance.userprofile.save()


post_save.connect(create_profile, sender=User)