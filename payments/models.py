from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=False)
    sender = models.OneToOneField(User, on_delete=models.SET_NULL)
    recipient = models.OneToOneField(User, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now=True)
    validated_at = models.DateField()
    details = models.TextField(max_length=256)

    def __str__(self):
        return "Transaction id : {0} - Amount : {1}".format(self.transaction_id, self.amount)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=False)
    sender = models.OneToOneField(User, on_delete=models.SET_NULL)
    recipient = models.OneToOneField(User, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now=True)
    validated_at = models.DateField()
    details = models.TextField(max_length=256)

    def __str__(self):
        return "Payment id : {0} - Amount : {1}".format(self.payment_id, self.amount)


class CaseIssue(models.Model):
    case_id = models.AutoField(primary_key=True)
    participant_1 = models.ForeignKey(User, null=True , on_delete = models.SET_NULL)
    participant_2 = models.ForeignKey(User, null=True , on_delete = models.SET_NULL)
    amount = models.IntegerField()
    subject = models.TextField(max_length=32)
    description = models.TextField(max_length=256)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    closed_at = models.DateField()

    def __str__(self):
        return "CaseIssue id : {0} - Participant 1 : {1}, Participant 2 : {2}".format(self.case_id, self.participant_1, self.participant_2)



class Reduction(models.Model):
    reduction_id = models.AutoField(primary_key=True)
    code = models.TextField(max_length=8)
    percent =  models.DecimalField(max_digits=10, decimal_places=5)
    user = models.ForeignKey(User, null=True , on_delete = models.SET_NULL)
    created_at = models.DateField(auto_now=True) 
    used_at = models.DateField()

    def __str__(self):
        return "Reduction id : {0} - percent : {1}".format(self.reduction_id, self.percent)
