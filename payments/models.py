from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from pay import settings
from pay import utils
import uuid


HELP_TEXT_FOR_DATE ="Please use the following format: <em>YYYY-MM-DD</em>."
HELP_TEXT_FOR_SERVICE_REF_NUMBER = 'Please enter the reference number issued by the operation.'
HELP_TEXT_FOR_OPERATOR = 'Please enter the operator who is offering this service'
help_text=HELP_TEXT_FOR_CUSTOMER = 'Please enter the customer who is using this service'
help_text=HELP_TEXT_FOR_CUSTOMER_REF = 'Please enter the customer reference number used by the operator of this service'
help_text=HELP_TEXT_FOR_SERVICE_ISSUED_AT = 'Please enter the date when this bill was issued (following format: <em>YYYY-MM-DD</em>.)'

COMMISSION_DEFAULT = 0.03
COMMISSION_MAX_DIGITS = 3
COMMISSION_DECIMAL_PLACES = 2


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
    idcard_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return "Card id : {} User : {}".format(self.pk, self.user)
    
    def get_absolute_url(self):
        return reverse('payments:idcard-detail', kwargs={'idcard_uuid':self.idcard_uuid})
    
    def get_update_url(self):
        return reverse('payments:idcard-update', kwargs={'idcard_uuid':self.idcard_uuid})
    
    def get_dashboard_update_url(self):
        return reverse('dashboard:idcard-update', kwargs={'idcard_uuid':self.idcard_uuid})
    
    def get_dashboard_update_url(self):
        return reverse('dashboard:idcard-update', kwargs={'idcard_uuid':self.idcard_uuid})
   


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
    users = models.ForeignKey(User, related_name="policy", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    commission = models.DecimalField(max_digits=COMMISSION_MAX_DIGITS, decimal_places=COMMISSION_DECIMAL_PLACES, default=COMMISSION_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_policies", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    policy_uuid = models.UUIDField(default=uuid.uuid4, editable=False)



    def __str__(self):
        return "Policy {0}".format(self.commission)

    def get_absolute_url(self):
        return reverse("payments:policy-detail", kwargs={"policy_uuid": self.policy_uuid})
    
    def get_dashboard_absolute_url(self):
        return reverse("dashboard:policy-detail", kwargs={"policy_uuid": self.policy_uuid})
    
    def get_dashboard_remove_url(self):
        return reverse("dashboard:policy-remove", kwargs={"policy_uuid": self.policy_uuid})
    
    def get_dashboard_update_url(self):
        return reverse("dashboard:policy-update", kwargs={"policy_uuid": self.policy_uuid})


class PolicyGroup(models.Model):
    name = models.CharField(max_length=80)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='policy_group')
    members = models.ManyToManyField(User, through='PolicyMembership')
    policy_group_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class PolicyMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_group = models.ForeignKey(PolicyGroup, on_delete=models.CASCADE)
    policy_membership_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_code = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_categories", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, related_name="created_categories", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    category_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return "ServiceCategory " + self.category_name
    
    def get_absolute_url(self):
        return reverse("payments:service-categories-detail", kwargs={"category_uuid": self.category_uuid})
    
    def get_dashboard_absolute_url(self):
        return reverse("dashboard:category-service-detail", kwargs={"category_uuid": self.category_uuid})

    def get_dashboard_update_url(self):
        return reverse("dashboard:category-service-update", kwargs={"category_uuid": self.category_uuid})
    
    def get_dashboard_remove_url(self):
        return reverse("dashboard:category-service-remove", kwargs={"category_uuid": self.category_uuid})
    


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
    service_code = models.IntegerField()
    name = models.CharField(max_length=50)
    operator = models.ForeignKey(User, related_name="available_services", unique=False,null=True,  on_delete=models.CASCADE, help_text=HELP_TEXT_FOR_OPERATOR)
    category = models.ForeignKey(ServiceCategory, related_name="available_services", unique=False, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_services", unique=False, null=True, on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_available_services", unique=False, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=80, blank=True, null=True)
    available_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return "AvailableService " + self.name
    
    def get_absolute_url(self):
        """
        This method returns the url that is used to query the details of this models.
        """
        return reverse('payments:available-service-detail', kwargs={'available_uuid':self.available_uuid})
    
    def get_usage_url(self):
        """
        This method returns the url that is used to query the details of this models.
        """
        return reverse('payments:new-service', kwargs={'available_service_uuid':self.available_uuid})

    def get_dashboard_absolute_url(self):
        """
        This method returns the url that is used to query the details of this models.
        """
        return reverse('dashboard:available-service-detail', kwargs={'available_uuid':self.available_uuid})

    def get_dashboard_remove_url(self):
        return reverse('dashboard:available-service-remove', kwargs={'available_uuid':self.available_uuid})

    def get_dashboard_update_url(self):
        return reverse('dashboard:available-service-update', kwargs={'available_uuid':self.available_uuid})
    
    
    def get_link(self):
        """
        This method returns the link that let the user use this services.
        """
        return reverse('payments:new-service', kwargs={'available_uuid':self.available_uuid})
    


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
    name = models.CharField(max_length=50, null=True)
    operator = models.ForeignKey(User,null=True, related_name="offered_services", unique=False, on_delete=models.CASCADE, help_text=HELP_TEXT_FOR_OPERATOR)
    customer = models.ForeignKey(User,null=True, related_name="used_services", unique=False, on_delete=models.CASCADE, help_text=HELP_TEXT_FOR_CUSTOMER)
    reference_number = models.IntegerField(help_text=HELP_TEXT_FOR_SERVICE_REF_NUMBER)
    customer_reference = models.CharField(max_length=50, null=True, help_text=HELP_TEXT_FOR_CUSTOMER_REF)
    category = models.ForeignKey(ServiceCategory, related_name="category_services", unique=False, null=True, on_delete=models.SET_NULL)
    service_instance = models.ForeignKey(AvailableService,null=True, related_name="executed_services", unique=False, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    commission = models.DecimalField(max_digits=COMMISSION_MAX_DIGITS, decimal_places=COMMISSION_DECIMAL_PLACES, default=COMMISSION_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    issued_at = models.DateField(help_text=HELP_TEXT_FOR_SERVICE_ISSUED_AT)
    description = models.CharField(max_length=80, null=True)
    verification_code = models.TextField(max_length=80, default=utils.generate_token_10)
    service_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return "Service " + self.name
    
    def get_absolute_url(self):
        return reverse('payments:service-detail', kwargs={'service_uuid':self.service_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:service-detail', kwargs={'service_uuid':self.service_uuid})

class Reduction(models.Model):
    code = models.TextField(max_length=8)
    percent =  models.DecimalField(max_digits=COMMISSION_MAX_DIGITS, decimal_places=COMMISSION_DECIMAL_PLACES, default=COMMISSION_DEFAULT)
    user = models.ForeignKey(User, null=True , on_delete = models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField()
    reduction_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "Reduction {}".format( self.percent)
    
    def get_absolute_url(self):
        return reverse('payments:reduction-detail', kwargs={'reduction_uuid':self.reduction_uuid})


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
    transaction_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "Transaction id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    def get_absolute_url(self):
        return reverse('payments:transaction-detail', kwargs={'transaction_uuid':self.transaction_uuid})


class Payment(models.Model):
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_payments')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_payments')
    verification_code = models.TextField(max_length=80, default=utils.generate_token_10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(auto_now=True)
    details = models.TextField(max_length=256)
    payment_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "Payment id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    def get_absolute_url(self):
        return reverse('payments:payment-detail', kwargs={'payment_uuid':self.payment_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:payment-detail', kwargs={'payment_uuid':self.payment_uuid})

class Transfer(models.Model):
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_transfers')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_transfers')
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField(max_length=256)
    verification_code = models.TextField(max_length=80, default=utils.generate_token_10, editable=False)
    transfer_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "Transfer  - Amount : {}".format(self.amount)

    def get_absolute_url(self):
        return reverse('payments:transfer-detail', kwargs={'transfer_uuid':self.transfer_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:transfer-detail', kwargs={'transfer_uuid':self.transfer_uuid})

class CaseIssue(models.Model):
    participant_1 = models.ForeignKey(User, null=True , on_delete = models.CASCADE, related_name='created_issues')
    participant_2 = models.ForeignKey(User, null=True , on_delete = models.CASCADE, related_name='complaints')
    amount = models.IntegerField()
    subject = models.TextField(max_length=32)
    description = models.TextField(max_length=256)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now=True)
    issue_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "CaseIssue id : {0} - Participant 1 : {1}, Participant 2 : {2}".format(self.pk, self.participant_1, self.participant_2)

    def get_absolute_url(self):
        return reverse('payments:case-detail', kwargs={'issue_uuid':self.issue_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:case-detail', kwargs={'issue_uuid':self.issue_uuid})

    def get_dashboard_close_url(self):
        return reverse('dashboard:case-close', kwargs={'issue_uuid':self.issue_uuid})



