from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.urls import reverse
import uuid

# Create your models here.

class Voucher(models.Model):
    name = models.CharField(max_length=32, blank=False)
    voucher_code = models.TextField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=False, null=False)
    activated = models.BooleanField(default=False)
    activated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_used = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    activated_by = models.ForeignKey(User, related_name='acticatedvouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    used_by = models.ForeignKey(User, related_name='usedvouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    sold_by = models.ForeignKey(User, related_name='soldvouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    used_at = models.DateTimeField(blank=True, null=True)
    sold_at = models.DateTimeField(blank=True, null=True)
    voucher_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("voucher:voucher-detail", kwargs={"voucher_uuid": self.voucher_uuid})


class SoldVoucher(models.Model):

    seller = models.ForeignKey(User, related_name='sold_vouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey(Voucher, related_name="sold_vouchers", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    sold_at = models.DateTimeField(auto_now_add=True)
    voucher_uuid = models.UUIDField(default=uuid.uuid4,editable=False)

    class Meta:
        verbose_name = _("SoldVoucher")
        verbose_name_plural = _("SoldVouchers")
        

    def __str__(self):
        return self.voucher.name

    def get_absolute_url(self):
        return reverse("voucher:sold-voucher-detail", kwargs={"voucher_uuid": self.voucher_uuid})



class UsedVoucher(models.Model):

    customer = models.ForeignKey(User, related_name='used_vouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey(Voucher, related_name="used_vouchers", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    used_at = models.DateTimeField(auto_now_add=True)
    voucher_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    class Meta:
        verbose_name = _("UsedVoucher")
        verbose_name_plural = _("UsedVouchers")
        

    def __str__(self):
        return self.voucher.name

    def get_absolute_url(self):
        return reverse("voucher:used-voucher-detail", kwargs={"voucher_uuid": self.voucher_uuid})


class Recharge(models.Model):
    voucher = models.ForeignKey(Voucher, related_name="recharges", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(User, related_name='customer_recharges', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(User, related_name='recharges', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    amount = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    recharge_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "Recharge " + self.voucher.name

    def get_absolute_url(self):
        return reverse("voucher:recharge-detail", kwargs={"recharge_uuid": self.recharge_uuid})
    
