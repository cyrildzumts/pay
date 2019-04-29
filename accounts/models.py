from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import uuid

# Create your models here.
class Policy(models.Model):
    daily_limit = models.IntegerField(blank=False)
    weekly_limit = models.IntegerField(blank=False)
    monthly_limit = models.IntegerField(blank=False)
    commission = models.DecimalField(max_digits=10, decimal_places=5, default=3.0)

    def __str__(self):
        return "Policy id : {0} - Commission : {1}".format(self.policy_id, self.commission)
    



class Account(models.Model):
    ACCOUNT_TYPE = (
        ('P', 'Privé'),
        ('B', 'Business'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(default='', max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(default='', max_length=50, blank=True, null=True)
    address = models.CharField(default='', max_length=50,null=True)
    zip_code = models.CharField(default='', max_length=15, blank=True, null=True)
    telefon = models.CharField(default='', max_length=15, null=True, blank=True)
    newsletter = models.BooleanField(default=False)
    is_active_account = models.BooleanField(default=True, blank=True, null=True)
    solde = models.IntegerField(default=0)
    created_at = models.DateField(auto_now=True)
    account_type = models.CharField(max_length=1, default='P', blank=False, null=False, choices=ACCOUNT_TYPE)
    policy = models.ForeignKey(Policy, related_name="policy", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    #account_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    class Meta:
        permissions = (
            ('deactivate_account', "Can deactivate a User"),
        )

    def __str__(self):
        return "Account : {}".format(self.user)


    def get_absolute_url(self):
        return reverse('accounts:edit_account', args=[str(self.pk)])


    
class IDCard(models.Model):
    card_number = models.IntegerField(blank=False)
    image = models.ImageField(blank=False)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Card id : {} User : {}".format(self.card_id, self.user)




@receiver(post_save, sender=User)
def create_or_update_account(sender,instance, created,  **kwargs):
    """
    This slot is called whenever a new User is created.
    There are two way to create a new user : From the Admin Site and 
    from A views. When a new User is created from the Admin Site, an account 
    profile is also created, so we don't have create an associated account again when
    this slot is executed.
    When a new User created from a views or programmatically, there is no associated account 
    to the new user, so we have to create a new account for that user.
    """

    print("New user  signal")
    print("sender is superuser: {}".format(sender.is_superuser))
    
    if created:
        print("New user was created")
        print("user being created : {}".format(instance.username))
        # first check if instance already has a account profile
        # if the user hasn't an associated account profile then we create an Profile account.
        #
        if not Account.objects.filter(user=instance).exists():
            print("This user is not beeing created by admin")
            Account.objects.create(user=instance)
        else:
            print("This user is beeing created by admin")
        

