from django.db import models

# Create your models here.
class AccessPermissions(models.Model):

    class Meta:
        managed = False
        permissions = {
            ('can_view_dashboard', 'Can view Dashboard'),
            ('can_create_group', 'Can create a Group'),
            ('can_change_group', 'Can change a Group'),
            ('can_delete_group', 'Can delete a Group'),
            ('can_view_voucher', 'Can view Voucher'),
            ('can_delete_voucher', 'Can delete Voucher'),
            ('can_change_voucher', 'Can change Voucher'),
            ('can_create_voucher', 'Can create Voucher'),
            ('can_activate_voucher', 'Can activate Voucher'),
            ('can_recharge_account', 'Can recharge an Account'),

        }