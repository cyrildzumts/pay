from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.urls import reverse

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

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")
        permissions = (
            ('can_add_voucher', "Can add  an voucher"),
            ('can_view_voucher', "Can read  an voucher"),
            ('can_change_voucher', "Can change  an voucher"),
            ('can_delete_voucher', "Can delete an voucher"),
            ('can_activate_voucher', 'Can activate voucher'),
            ('can_sell_voucher', 'Can sell voucher'),
            ('api_add_voucher', "Can add  an voucher through rest api"),
            ('api_view_voucher', 'Can read through a rest api'),
            ('api_change_voucher', 'Can edit through a rest api'),
            ('api_delete_voucher', 'Can delete through a rest api'),
            ('api_activate_voucher', 'Can activate voucher through rest api'),
            ('api_sell_voucher', 'Can sell voucher through rest api'),
        )


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("voucher:voucher_details", kwargs={"pk": self.pk})


class SoldVoucher(models.Model):

    seller = models.ForeignKey(User, related_name='sold_vouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey(Voucher, related_name="sold_vouchers", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    sold_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("SoldVoucher")
        verbose_name_plural = _("SoldVouchers")
        permissions = (
            ('can_add_soldevoucher', "Can add  an soldevoucher"),
            ('can_view_soldevoucher', "Can read  an soldevoucher"),
            ('can_change_soldevoucher', "Can change  an soldevoucher"),
            ('can_delete_soldevoucher', "Can delete an soldevoucher"),
            ('api_add_soldevoucher', "Can add  an soldevoucher through rest api"),
            ('api_view_soldevoucher', 'Can read through a rest api'),
            ('api_change_soldevoucher', 'Can edit through a rest api'),
            ('api_delete_soldevoucher', 'Can delete through a rest api'),
        )

    def __str__(self):
        return self.voucher.name

    def get_absolute_url(self):
        return reverse("voucher:sold_voucher_details", kwargs={"pk": self.pk})



class UsedVoucher(models.Model):

    customer = models.ForeignKey(User, related_name='used_vouchers', unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    voucher = models.ForeignKey(Voucher, related_name="used_vouchers", unique=False, null=True,blank=True, on_delete=models.SET_NULL)
    used_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _("UsedVoucher")
        verbose_name_plural = _("UsedVouchers")
        permissions = (
            ('can_add_usedvoucher', "Can add  an usedvoucher"),
            ('can_view_usedvoucher', "Can read  an usedvoucher"),
            ('can_change_usedvoucher', "Can change  an usedvoucher"),
            ('can_delete_usedvoucher', "Can delete an usedvoucher"),
            ('api_add_usedvoucher', "Can add  an usedvoucher through rest api"),
            ('api_view_usedvoucher', 'Can read through a rest api'),
            ('api_change_usedvoucher', 'Can edit through a rest api'),
            ('api_delete_usedvoucher', 'Can delete through a rest api'),
        )

    def __str__(self):
        return self.voucher.name

    def get_absolute_url(self):
        return reverse("voucher:used_voucher_details", kwargs={"pk": self.pk})
