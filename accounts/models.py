from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.
class Policy(models.Model):
    policy_id = models.AutoField(primary_key=True)
    daily_limit = models.IntegerField(blank=False)
    weekly_limit = models.IntegerField(blank=False)
    monthly_limit = models.IntegerField(blank=False)
    commission = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return "Policy id : {0} - Commission : {1}".format(self.policy_id, self.commission)
    



class Account(models.Model):
    ACCOUNT_TYPE = (
        ('P', 'Privé'),
        ('B', 'Business'),
    )
    account_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    country = models.CharField(default='', max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    province = models.CharField(default='', max_length=50, blank=True)
    address = models.CharField(default='', max_length=50)
    zip_code = models.CharField(default='', max_length=15, blank=True)
    telefon = models.CharField(default='', max_length=15)
    newsletter = models.BooleanField(default=False)
    is_active_account = models.BooleanField(default=True)
    solde = models.IntegerField(default=0)
    created_at = models.DateField(auto_now=True)
    account_type = models.CharField(max_length=1, default='P', blank=False, null=False, choices=ACCOUNT_TYPE)
    policy = models.ForeignKey(Policy, related_name="policy", unique=False, null=True, on_delete=models.SET_NULL)


    class Meta:
        permissions = (
            ('deactivate_account', "Can deactivate a User"),
        )

    def __str__(self):
        return "Account : {}".format(self.user)


    def get_absolute_url(self):
        return reverse('accounts:edit_account', args=[str(self.pk)])


    
class IDCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_number = models.IntegerField(blank=False)
    image = models.ImageField(blank=False)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Card id : {} User : {}".format(self.card_id, self.user)





def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        #user_profil = UserProfile(user=user)
        #user_profil.save()
        Account.objects.create(user=user)

