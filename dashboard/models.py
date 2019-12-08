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
            (Constants.VOUCHER_RECHARGE_ACCOUNT_PERM, 'Can recharge an Account'),

            (Constants.AVAILABLE_SERVICE_VIEW_PERM, 'Dashboard Can View Available Service'),
            (Constants.AVAILABLE_SERVICE_CHANGE_PERM, 'Dashboard Can Change Available Service'),
            (Constants.AVAILABLE_SERVICE_ADD_PERM, 'Dashboard Can Add Available Service'),
            (Constants.AVAILABLE_SERVICE_DELETE_PERM, 'Dashboard Can Delete Available Service'),

            (Constants.SERVICE_VIEW_PERM, 'Dashboard Can View Service'),
            (Constants.SERVICE_CHANGE_PERM, 'Dashboard Can Change Service'),
            (Constants.SERVICE_ADD_PERM, 'Dashboard Can Add Service'),
            (Constants.SERVICE_DELETE_PERM, 'Dashboard Can Delete Service'),

            (Constants.TRANSFER_VIEW_PERM, 'Dashboard Can View Transfer'),
            (Constants.TRANSFER_CHANGE_PERM, 'Dashboard Can Change Transfer'),
            (Constants.TRANSFER_ADD_PERM, 'Dashboard Can Add Transfer'),
            (Constants.TRANSFER_DELETE_PERM, 'Dashboard Can Delete Transfer'),

            (Constants.CATEGORY_VIEW_PERM, 'Dashboard Can View Category'),
            (Constants.CATEGORY_CHANGE_PERM, 'Dashboard Can Change Category'),
            (Constants.CATEGORY_ADD_PERM, 'Dashboard Can Add Category'),
            (Constants.CATEGORY_DELETE_PERM, 'Dashboard Can Delete Category'),

            (Constants.POLICY_VIEW_PERM, 'Dashboard Can View Policy'),
            (Constants.POLICY_CHANGE_PERM, 'Dashboard Can Change Policy'),
            (Constants.POLICY_ADD_PERM, 'Dashboard Can Add Policy'),
            (Constants.POLICY_DELETE_PERM, 'Dashboard Can Delete Policy'),



        ]