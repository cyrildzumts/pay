from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from pay import settings
from pay import utils
from pay import conf as GLOBAL_CONF
from payments import constants as Constants
import uuid
import datetime



def ident_file_path(instance, filename):
    file_ext = filename.split(".")[-1]
    name = settings.IDENTIFICATION_DOC_NAME_PREFIX + "." + file_ext
    return "identifications/pay_user_{0}_{1}".format(instance.user.id, name)



class Balance(models.Model):
    name = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    balance = models.DecimalField(default=0.0,blank=False, null=False, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    balance_without_fee = models.DecimalField(default=0.0,blank=False, null=False, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    balance_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("payments:balance-detail", kwargs={"balance_uuid": self.balance_uuid})
    
    def get_history_url(self):
        return reverse('payments:balance-history', kwargs={'balance_uuid':self.balance_uuid})

class BalanceHistory(models.Model):
    balance_ref_id = models.IntegerField(blank=False, null=False)
    current_amount = models.DecimalField(blank=False, null=False, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    current_amount_without_fee = models.DecimalField(blank=False, null=False, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    is_incoming = models.BooleanField(default=False, blank=True, null=True)
    balance_amount = models.DecimalField(blank=False, null=False, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    balance_amount_without_fee = models.DecimalField(default=0.0,blank=False, null=False, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    sender = models.ForeignKey(User, related_name='sender_histories', blank=True, null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, related_name='receiver_histories', blank=True, null=True, on_delete=models.SET_NULL)
    activity = models.IntegerField(default=Constants.BALANCE_ACTIVITY_RECHARGE, choices=Constants.BALANCE_ACTIVITY_TYPES)
    balance = models.ForeignKey(Balance, related_name="balance_history", blank=True, null=True, on_delete=models.SET_NULL)
    recharge = models.ForeignKey('voucher.Recharge', related_name='balance_history', null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey('voucher.Voucher', related_name="balance_history", blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    history_uuid = models.UUIDField(default=uuid.uuid4, editable=False)    


    def __str__(self):
        if self.is_incoming:
            return f"{self.created_at.isoformat(' ', 'seconds')}  -  {self.sender.username}  -  {utils.find_element_by_key_in_tuples(self.activity, Constants.BALANCE_ACTIVITY_TYPES)}  -  -{self.current_amount} {_(settings.CURRENCY)}"
        return f"{self.created_at.isoformat(' ', 'seconds')}  -  {self.receiver.username}  -  {utils.find_element_by_key_in_tuples(self.activity, Constants.BALANCE_ACTIVITY_TYPES)}  -  -{self.current_amount} {_(settings.CURRENCY)}"

    def get_absolute_url(self):
        return reverse("payments:activity-details", kwargs={"history_uuid": self.history_uuid})
    
    def get_dashboard_url(self):
        return reverse("dashboard:activity-details", kwargs={"history_uuid": self.history_uuid})


    
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
    validated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,related_name='validated_idcards')
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
    
    @property
    def has_expired(self):
        return self.expire_at < datetime.date.today()
   


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
    commission = models.DecimalField(max_digits=Constants.COMMISSION_MAX_DIGITS, decimal_places=Constants.COMMISSION_DECIMAL_PLACES, default=Constants.COMMISSION_DEFAULT)
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
    group_type = models.IntegerField(default=Constants.POLICY_GROUP_BASIC, choices=Constants.POLICY_GROUP)
    members = models.ManyToManyField(User, through='PolicyMembership', through_fields=('group', 'user'), blank=True)
    policy_group_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("payments:policy-group", kwargs={"group_uuid": self.policy_group_uuid})
    
    def get_dashboard_absolute_url(self):
        return reverse("dashboard:policy-group-detail", kwargs={"group_uuid": self.policy_group_uuid})

    def get_dashboard_update_url(self):
        return reverse("dashboard:policy-group-update", kwargs={"group_uuid": self.policy_group_uuid})
    
    def get_dashboard_remove_url(self):
        return reverse("dashboard:policy-group-remove", kwargs={"group_uuid": self.policy_group_uuid})



class PolicyMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PolicyGroup, on_delete=models.CASCADE)
    policy_membership_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="modified_membership", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    added_by = models.ForeignKey(User, related_name="added_membership", unique=False, null=True,blank=True, on_delete=models.SET_NULL)


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
    operator = models.ForeignKey(User, related_name="available_services", unique=False,null=True,  on_delete=models.CASCADE, help_text=Constants.HELP_TEXT_FOR_OPERATOR)
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
    operator = models.ForeignKey(User,null=True, related_name="offered_services", unique=False, on_delete=models.CASCADE, help_text=Constants.HELP_TEXT_FOR_OPERATOR)
    customer = models.ForeignKey(User,null=True, related_name="used_services", unique=False, on_delete=models.CASCADE, help_text=Constants.HELP_TEXT_FOR_CUSTOMER)
    reference_number = models.IntegerField(help_text=Constants.HELP_TEXT_FOR_SERVICE_REF_NUMBER, blank=True, null=True)
    customer_reference = models.CharField(max_length=50, blank=True ,null=True, help_text=Constants.HELP_TEXT_FOR_CUSTOMER_REF)
    category = models.ForeignKey(ServiceCategory, related_name="category_services", unique=False, null=True, on_delete=models.SET_NULL)
    service_instance = models.ForeignKey(AvailableService,null=True, related_name="executed_services", unique=False, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    commission = models.DecimalField(max_digits=Constants.COMMISSION_MAX_DIGITS, decimal_places=Constants.COMMISSION_DECIMAL_PLACES, default=Constants.COMMISSION_DEFAULT, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    issued_at = models.DateField(help_text=Constants.HELP_TEXT_FOR_SERVICE_ISSUED_AT, blank=True, null=True)
    description = models.CharField(max_length=80, null=True)
    verification_code = models.TextField(max_length=80, default=utils.generate_token_10)
    service_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return "Service " + self.name
    
    def get_absolute_url(self):
        return reverse('payments:service-detail', kwargs={'service_uuid':self.service_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:service-detail', kwargs={'service_uuid':self.service_uuid})
    
    @staticmethod
    def get_user_services(user):
        queryset = Service.objects.none()
        if isinstance(user, User) and user.is_authenticated:
            queryset = Service.objects.filter(Q(customer=user) | Q(operator=user)).order_by('-created_at')
        return queryset

class Reduction(models.Model):
    code = models.TextField(max_length=8)
    percent =  models.DecimalField(max_digits=Constants.COMMISSION_MAX_DIGITS, decimal_places=Constants.COMMISSION_DECIMAL_PLACES, default=Constants.COMMISSION_DEFAULT)
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
    amount = models.DecimalField(default=0.0, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    fee = models.DecimalField(blank=True, null=True, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_payments')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_payments')
    verification_code = models.TextField(max_length=80, default=utils.generate_token_10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(auto_now=True)
    details = models.TextField(max_length=256)
    payment_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Payment - {self.amount}"
    
    def get_absolute_url(self):
        return reverse('payments:payment-detail', kwargs={'payment_uuid':self.payment_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:payment-detail', kwargs={'payment_uuid':self.payment_uuid})

    @staticmethod
    def get_user_payments(user):
        queryset = Payment.objects.none()
        if user and user.is_authenticated:
            queryset = Payment.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-created_at')
        return queryset



class PaymentRequest(models.Model):
    """
    A PaymentRequest object is only used by partner and is created per REST request.
    A payment request can be accepted and paid by the customer who is receiving this
    payment request.
    """
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE, blank=True, null=True)
    verification_code = models.TextField(max_length=80, default=utils.generate_token_10, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE ,blank=False )
    requester_name = models.CharField(max_length=32 ,blank=True, null=True)
    amount = models.DecimalField(default=0.0,max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    unit_price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    tva = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    commission = models.DecimalField(max_digits=5,decimal_places=4, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default=Constants.PR_CREATED, blank=True, null=False)
    product_name = models.CharField(max_length=255 ,blank=False, null=False)
    customer_name = models.CharField(max_length=255 ,blank=False, null=False)
    description = models.CharField(max_length=255 ,blank=False, null=False)
    redirect_success_url = models.TextField(max_length=256, blank=True, null=True)
    redirect_failed_url = models.TextField(max_length=256, blank=True, null=True)
    failed_reason = models.TextField(max_length=256, blank=True, null=True)
    request_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return "Payment Request id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    #def get_absolute_url(self):
    #    return reverse('payments:payment-detail', kwargs={'payment_uuid':self.payment_uuid})

    def get_dashboard_url(self):
        return reverse('dashboard:payment-request-detail', kwargs={'request_uuid':self.request_uuid})

    @staticmethod
    def get_user_payments(user):
        queryset = PaymentRequest.objects.none()
        if user and user.is_authenticated:
            queryset = PaymentRequest.objects.filter(Q(seller=user) | Q(payment__recipient=user))
        return queryset


class ExternalPayment(models.Model):
    payment_request = models.OneToOneField('PaymentRequest', on_delete=models.CASCADE)
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    request_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "External Payment : {0} - Amount : {1}".format(self.pk, self.payment.amount)
    
    #def get_absolute_url(self):
    #    return reverse('payments:payment-detail', kwargs={'payment_uuid':self.payment_uuid})

    #def get_dashboard_url(self):
    #    return reverse('dashboard:external-payment-request-detail', kwargs={'request_uuid':self.request_uuid})


class Transfer(models.Model):
    amount = models.DecimalField(default=0.0, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
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

    @staticmethod
    def get_user_transfers(user):
        queryset = Transfer.objects.none()
        if user and user.is_authenticated:
            queryset = Transfer.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-created_at')
        return queryset


class Refund(models.Model):
    amount = models.DecimalField(default=0.0, max_digits=GLOBAL_CONF.MAX_DIGITS, decimal_places=GLOBAL_CONF.DECIMAL_PLACES)
    status = models.IntegerField(default=Constants.REFUND_PENDING, choices=Constants.REFUND_STATUS)
    declined_reason = models.IntegerField(blank=True, null=True, choices=Constants.REFUND_DECLINED_REASON)
    payment = models.OneToOneField('payments.Payment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_changed_at = models.DateTimeField(auto_now=True)
    refund_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Refund {self.payment.sender.username} - {self.payment.recipient.username} : {self.amount} {settings.CURRENCY}"

    def get_absolute_url(self):
        return reverse('payments:refund-detail', kwargs={'refund_uuid':self.refund_uuid})

    def get_dashboard_absolute_url(self):
        return reverse('dashboard:refund-detail', kwargs={'refund_uuid':self.refund_uuid})


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



