from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Voucher(models.Model):
    voucher_id = models.IntegerField(primary_key=True)
    voucher_code = models.TextField(max_length=18)
    created_at = models.DateField(auto_now=True)
    used_at = models.DateField()
    user = models.ForeignKey(User)
    is_used = models.BooleanField(default=False)