from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Transaction(models.Model):
    transaction_id = models.IntegerField(blank=False)
    amount = models.IntegerField(blank=False)
    sender = models.OneToOneField(User)
    recipient = models.OneToOneField(User)
    created_at = models.DateField(auto_now=True)
    validated_at = models.DateField()
    details = models.TextField(max_length=256)


class Payment(models.Model):
    transaction_id = models.IntegerField(blank=False)
    amount = models.IntegerField(blank=False)
    sender = models.OneToOneField(User)
    recipient = models.OneToOneField(User)
    created_at = models.DateField(auto_now=True)
    validated_at = models.DateField()
    details = models.TextField(max_length=256)


class CaseIssue(models.Model):
    case_id = models.IntegerField(primary_key=True)
    participant_1 = models.ForeignKey(User)
    participant_2 = models.ForeignKey(User)
    amount = models.IntegerField()
    subject = models.TextField(max_length=32)
    description = models.TextField(max_length=256)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    closed_at = models.DateField()



class Reduction(models.Model):
    reduction_id = models.IntegerField(primary_key=True)
    code = models.TextField(max_length=8)
    percent = models.DecimalField()
    user = models.ForeignKey(User)
    created_at = models.DateField(auto_now=True) 
    used_at = models.DateField()
