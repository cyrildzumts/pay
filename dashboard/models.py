from django.db import models
from dashboard import Constants


# Create your models here.
class AccessPermissions(models.Model):
   


    class Meta:
        managed = False
        permissions = [
            (Constants.DASHBOARD_VIEW_PERM, 'Can view Dashboard'),
            (Constants.GROUP_ADD_PERM, 'Can create a Group'),
            (Constants.GROUP_CHANGE_PERM, 'Can change a Group'),
            (Constants.GROUP_DELETE_PERM, 'Can delete a Group'),
            (Constants.GROUP_VIEW_PERM, 'Can view Group'),
            (Constants.VOUCHER_VIEW_PERM, 'Can view Voucher'),
            (Constants.VOUCHER_DELETE_PERM, 'Can delete Voucher'),
            (Constants.VOUCHER_CHANGE_PERM, 'Can change Voucher'),
            (Constants.VOUCHER_ADD_PERM, 'Can create Voucher'),
            (Constants.TOKEN_GENERATE_PERM, 'Can generate Token'),
            (Constants.VOUCHER_ACTIVATE_PERM, 'Can activate Voucher'),
            (Constants.VOUCHER_RECHARGE_ACCOUNT_PERM, 'Can recharge an Account')

        ]