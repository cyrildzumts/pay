from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Reduction(models.Model):
    code = models.TextField(max_length=8)
    percent =  models.DecimalField(max_digits=10, decimal_places=5)
    account = models.ForeignKey('accounts.Account', null=True , on_delete = models.SET_NULL)
    created_at = models.DateField(auto_now=True) 
    used_at = models.DateField()

    def __str__(self):
        return "Reduction {}".format( self.percent)
    
    def get_absolute_url(self):
        return reverse('accounts:reduction_detail', kwargs={'pk':self.pk})


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('T', 'Transfert'),
        ('P', 'Payment'),
        ('S', 'Service'),
    )
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='outgoing_transactions')
    recipient = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='incoming_transactions')
    created_at = models.DateField(auto_now=True)
    validated_at = models.DateField()
    details = models.TextField(max_length=256)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    policy = models.ForeignKey('accounts.Policy', blank=True, null=True, on_delete=models.SET_NULL)
    reduction = models.ForeignKey('payments.Reduction', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Transaction id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    def get_absolute_url(self):
        return reverse('accounts:transaction_detail', kwargs={'pk':self.pk})


class Payment(models.Model):
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='customer')
    recipient = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(auto_now=True)
    details = models.TextField(max_length=256)

    def __str__(self):
        return "Payment id : {0} - Amount : {1}".format(self.pk, self.amount)
    
    def get_absolute_url(self):
        return reverse('accounts:payment_detail', kwargs={'pk':self.pk})


class Transfer(models.Model):
    amount = models.IntegerField(blank=False)
    sender = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='transfer_sender')
    recipient = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='transfer_recipient')
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField(max_length=256)

    def __str__(self):
        return "Transfer id : {0} - Amount : {1}".format(self.pk, self.amount)

    def get_absolute_url(self):
        return reverse('accounts:transfer_detail', kwargs={'pk':self.pk})

class CaseIssue(models.Model):
    participant_1 = models.ForeignKey('accounts.Account', null=True , on_delete = models.CASCADE, related_name='issue_creator')
    participant_2 = models.ForeignKey('accounts.Account', null=True , on_delete = models.CASCADE, related_name='issue_participant')
    amount = models.IntegerField()
    subject = models.TextField(max_length=32)
    description = models.TextField(max_length=256)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "CaseIssue id : {0} - Participant 1 : {1}, Participant 2 : {2}".format(self.pk, self.participant_1, self.participant_2)

    def get_absolute_url(self):
        return reverse('accounts:case_detail', kwargs={'pk':self.pk})



