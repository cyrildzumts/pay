from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.

class Voucher(models.Model):
    name = models.CharField(max_length=32, blank=False)
    voucher_code = models.TextField(max_length=18)
    created_at = models.DateField(auto_now=True)
    amount = models.IntegerField(blank=False, null=False)
    activated = models.BooleanField(default=False)
    activated_at = models.DateField(blank=True, null=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("voucher_details", kwargs={"pk": self.pk})


class SoldVoucher(models.Model):

    seller = models.ForeignKey(User, related_name='sold_vouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey(Voucher, related_name="sold_vouchers", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    sold_at = models.DateField()

    class Meta:
        verbose_name = _("SoldVoucher")
        verbose_name_plural = _("SoldVouchers")

    def __str__(self):
        return self.voucher.name

    def get_absolute_url(self):
        return reverse("sold_voucher_detail", kwargs={"pk": self.pk})



class UsedVoucher(models.Model):

    customer = models.ForeignKey(User, related_name='used_vouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey(Voucher, related_name="used_vouchers", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    used_at = models.DateField()
    class Meta:
        verbose_name = _("UsedVoucher")
        verbose_name_plural = _("UsedVouchers")

    def __str__(self):
        return self.voucher.name

    def get_absolute_url(self):
        return reverse("used_voucher_detail", kwargs={"pk": self.pk})
