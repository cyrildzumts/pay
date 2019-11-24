from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from pay import settings
import uuid


def ident_file_path(instance, filename):
    file_ext = filename.split(".")[-1]
    name = settings.IDENTIFICATION_DOC_NAME_PREFIX + "." + file_ext
    return "identifications/pay_user_{0}_{1}".format(instance.user.id, name)
    
class IDCard(models.Model):
    card_number = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to=ident_file_path, blank=False)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL,related_name='idcard')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    delivery_at = models.DateField(blank=True, null=True)
    expire_at = models.DateField(blank=True, null=True)
    delivery_place = models.CharField(max_length=32, blank=True, null=True)
    is_valid = models.BooleanField(default=False, blank=True, null=True)
    idcard_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)
    
    class Meta:
        permissions = (
            ('api_view_idcard', 'Can read through a rest api'),
            ('api_change_idcard', 'Can edit through a rest api'),
            ('api_delete_idcard', 'Can delete through a rest api'),
        )

    def __str__(self):
        return "Card id : {} User : {}".format(self.pk, self.user)
    
    def get_absolute_url(self):
        return reverse('payments:idcard-detail', kwargs={'idcard_uuid':self.idcard_uuid})
    
    def get_update_url(self):
        return reverse('payments:idcard-update', kwargs={'idcard_uuid':self.idcard_uuid})
   


class Policy(models.Model):
    """
        Every Business account has a policy set. This policy defines the 
        transfer limit applied to the business account.
        For every transfer going to a business account a commission fee is extracted from 
        the transfer amount. This fee is added the PAY account.
        The daily_limit is maximal amount allowed to be received by a business account in a day.
        The weekly_limit is maximal amount allowed to be received by a business account in a week.
        The monthly_limit is maximal amount allowed to be received by a business account in a month.
        The commission is a percent value that is to be taken from the transfer amount.

    """
    daily_limit = models.IntegerField(blank=False)
    weekly_limit = models.IntegerField(blank=False)
    monthly_limit = models.IntegerField(blank=False)
    commission = models.DecimalField(max_digits=10, decimal_places=5, default=0.03)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_policies", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    policy_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)



    def __str__(self):
        return "{0}".format(self.commission)
    


class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True, null=False,blank=False)
    category_code = models.IntegerField(blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_categories", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, related_name="created_categories", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    category_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)


    def __str__(self):
        return self.category_name


class AvailableService(models.Model):
    """
    This model saves the available services. Each new available is saved in the database using this model.
    This model allows dynamics detection of newly added services.
    To make it easier to work with, a service is identified with a service code.
    The service code must be a unique value.
    template_name contains the name of the template used to render this service in html
    form_class contains the name of the Form used to interact with the service in html.
    operator_name is 
    """
    service_code = models.IntegerField(blank=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    operator = models.ForeignKey(User, related_name="available_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ServiceCategory, related_name="available_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    template_name = models.CharField(max_length=50, blank=True, null=True)
    form_class = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_available_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=80, blank=True, null=True)
    available_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    class Meta:
        permissions = (
            ('can_add_availableservice', "Can add an availableservice"),
            ('can_view_availableservice', "Can read an availableservice"),
            ('can_change_availableservice', "Can change an availableservice"),
            ('can_delete_availableservice', "Can delete an availableservice"),
            ('api_add_availableservice', "Can add  an availableservice through rest api"),
            ('api_view_availableservice', 'Can read through a rest api'),
            ('api_change_availableservice', 'Can edit through a rest api'),
            ('api_delete_availableservice', 'Can delete through a rest api'),
        )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        This method returns the url that is used to query the details of this models.
        """
        return reverse('payments:available-service-detail', kwargs={'available_uuid':self.available_uuid})
    
    def get_link(self):
        """
        This method returns the link that let the user use this services.
        """
        return reverse('payments:new-service', kwargs={'pk':self.pk})
    


class Service(models.Model):
    """
        A service is offered by an operator and is consumed by a customer.
        Both operator and customer are registered users.
        A service has an invoice which is identified by the operator with a reference number.
        Each consumed service has a price. The cost is substracted from the customer account.
        *A commision is applied to each service. The applied commission is defined by the policy 
        set to operator.
        *When an operator ses an ID number to reference his registered customer, the field customer_reference can be 
        used to save this ID.
        *The Field reference_number refers to the bill number as issued by the operator. Some business issue a
        whole integer as a bill number , some other issues an alpha-numeric value, this why this field is 
        represented with a CharField insteed of an IntegerField.

        * The field issued_at represents the date at which the operator has created the bill for which the customer
        is paying now.
        This model is accessible a User instance through 


    """
    name = models.CharField(max_length=50, blank=True, null=True)
    operator = models.ForeignKey(User, related_name="offered_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(User, related_name="used_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    reference_number = models.IntegerField(blank=False)
    customer_reference = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, related_name="category_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    service_instance = models.ForeignKey(AvailableService, related_name="executed_services", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    price = models.IntegerField(blank=False)
    commission = models.DecimalField(max_digits=10, decimal_places=5, default=3.0)
    created_at = models.DateTimeField(auto_now_add=True)
    issued_at = models.DateField()
    description = models.CharField(max_length=80, blank=True, null=True)
    service_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    class Meta:
        permissions = (
            ('can_add_service', "Can add an service"),
            ('can_view_service', "Can read an service"),
            ('can_change_service', "Can change an service"),
            ('can_delete_service', "Can delete an service"),
            ('api_add_service', "Can add  an service through rest api"),
            ('api_view_service', 'Can read through a rest api'),
            ('api_change_service', 'Can edit through a rest api'),
            ('api_delete_service', 'Can delete through a rest api'),
        )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('payments:service_detail', kwargs={'pk':self.pk})


class Reduction(models.Model):
    code = models.TextField(max_length=8)
    percent =  models.DecimalField(max_digits=10, decimal_places=5)
    account = models.ForeignKey(User, null=True , on_delete = models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField()
    reduction_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    def __str__(self):
        return "Reduction {}".format( self.percent)
    
    def get_absolute_url(self):
        return reverse('payments:reduction-detail', kwargs={'pk':self.pk})


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('T', 'Transfert'),
        ('P', 'Payment'),
        ('S', 'Service'),
    )
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_transactions')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    details = models.TextField(max_length=256)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    policy = models.ForeignKey(Policy, blank=True, null=True, on_delete=models.SET_NULL)
    reduction = models.ForeignKey(Reduction, blank=True, null=True, on_delete=models.SET_NULL)
    transaction_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    def __str__(self):
        return "Transaction id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    def get_absolute_url(self):
        return reverse('payments:transaction-detail', kwargs={'pk':self.pk})


class Payment(models.Model):
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_payments')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(auto_now=True)
    details = models.TextField(max_length=256)
    payment_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    def __str__(self):
        return "Payment id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    def get_absolute_url(self):
        return reverse('payments:payment-detail', kwargs={'pk':self.pk})


class Transfer(models.Model):
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_transfers')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_transfers')
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField(max_length=256)
    transfer_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    def __str__(self):
        return "Transfer id : {0} - Amount : {1}".format(self.pk, self.amount)

    def get_absolute_url(self):
        return reverse('payments:transfer-detail', kwargs={'pk':self.pk})

class CaseIssue(models.Model):
    participant_1 = models.ForeignKey(User, null=True , on_delete = models.CASCADE, related_name='created_issues')
    participant_2 = models.ForeignKey(User, null=True , on_delete = models.CASCADE, related_name='complaints')
    amount = models.IntegerField()
    subject = models.TextField(max_length=32)
    description = models.TextField(max_length=256)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now=True)
    issue_uuid = models.UUIDField(default=uuid.uuid4(), null=False, blank=False)

    def __str__(self):
        return "CaseIssue id : {0} - Participant 1 : {1}, Participant 2 : {2}".format(self.pk, self.participant_1, self.participant_2)

    def get_absolute_url(self):
        return reverse('payments:case-detail', kwargs={'pk':self.pk})



