from django.db import models


DASHBOARD_VIEW_PERM                 = 'dashboard.can_view_dashboard'
TOKEN_GENERATE_PERM                 = 'dashboard.can_generate_token'
ACCOUNT_VIEW_PERM                     = 'dashboard.can_view_account'
ACCOUNT_CREATE_PERM                   = 'dashboard.can_add_account'
ACCOUNT_CHANGE_PERM                   = 'dashboard.can_change_account'
ACCOUNT_DELETE_PERM                   = 'dashboard.can_delete_account'

CASE_ISSUE_VIEW_PERM                     = 'dashboard.can_view_claim'
CASE_ISSUE_CREATE_PERM                   = 'dashboard.can_add_claim'
CASE_ISSUE_CHANGE_PERM                   = 'dashboard.can_change_claim'
CASE_ISSUE_DELETE_PERM                   = 'dashboard.can_delete_claim'
CASE_ISSUE_CLOSE_PERM                    = 'dashboard.can_close_claim'

GROUP_VIEW_PERM                     = 'dashboard.can_view_group'
GROUP_ADD_PERM                   = 'dashboard.can_add_group'
GROUP_CHANGE_PERM                   = 'dashboard.can_change_group'
GROUP_DELETE_PERM                   = 'dashboard.can_delete_group'

IDCARD_VIEW_PERM                    = 'dashboard.can_view_idcard'
IDCARD_CREATE_PERM                  = 'dashboard.can_add_idcard'
IDCARD_CHANGE_PERM                  = 'dashboard.can_change_idcard'
IDCARD_DELETE_PERM                  = 'dashboard.can_delete_idcard'

VOUCHER_VIEW_PERM                   = 'dashboard.can_view_voucher'
VOUCHER_ADD_PERM                 = 'dashboard.can_add_voucher'
VOUCHER_CHANGE_PERM                 = 'dashboard.can_change_voucher'
VOUCHER_DELETE_PERM                 = 'dashboard.can_delete_voucher'
VOUCHER_ACTIVATE_PERM               = 'dashboard.can_activate_voucher'
VOUCHER_RECHARGE_ACCOUNT_PERM       = 'dashboard.can_recharge_account_voucher'

PAYMENT_VIEW_PERM                   = 'dashboard.can_view_payment'
PAYMENT_CREATE_PERM                 = 'dashboard.can_add_payment'
PAYMENT_CHANGE_PERM                 = 'dashboard.can_change_payment'
PAYMENT_DELETE_PERM                 = 'dashboard.can_delete_payment'

POLICY_VIEW_PERM                    = 'dashboard.can_view_policy'
POLICY_CREATE_PERM                  = 'dashboard.can_add_policy'
POLICY_CHANGE_PERM                  = 'dashboard.can_change_policy'
POLICY_DELETE_PERM                  = 'dashboard.can_delete_policy'

CATEGORY_VIEW_PERM                  = 'dashboard.can_view_category'
CATEGORY_CREATE_PERM                = 'dashboard.can_add_category'
CATEGORY_CHANGE_PERM                = 'dashboard.can_change_category'
CATEGORY_DELETE_PERM                = 'dashboard.can_delete_category'

AVAILABLE_SERVICE_VIEW_PERM         = 'dashboard.can_view_available_service'
AVAILABLE_SERVICE_CREATE_PERM       = 'dashboard.can_add_available_service'
AVAILABLE_SERVICE_CHANGE_PERM       = 'dashboard.can_change_available_service'
AVAILABLE_SERVICE_DELETE_PERM       = 'dashboard.can_delete_available_service'

SERVICE_VIEW_PERM                   = 'dashboard.can_view_service'
SERVICE_CREATE_PERM                 = 'dashboard.can_add_service'
SERVICE_CHANGE_PERM                 = 'dashboard.can_change_service'
SERVICE_DELETE_PERM                 = 'dashboard.can_delete_service'

TRANSFER_VIEW_PERM                  = 'dashboard.can_view_transfer'
TRANSFER_CREATE_PERM                = 'dashboard.can_add_transfer'
TRANSFER_CHANGE_PERM                = 'dashboard.can_change_transfer'
TRANSFER_DELETE_PERM                = 'dashboard.can_delete_transfer'

REDUCTION_VIEW_PERM                  = 'dashboard.can_view_reduction'
REDUCTION_CREATE_PERM                = 'dashboard.can_add_reduction'
REDUCTION_CHANGE_PERM                = 'dashboard.can_change_reduction'
REDUCTION_DELETE_PERM                = 'dashboard.can_delete_reduction'


# Create your models here.
class AccessPermissions(models.Model):
   


    class Meta:
        managed = False
        permissions = [
            (DASHBOARD_VIEW_PERM, 'Can view Dashboard'),
            (GROUP_ADD_PERM, 'Can create a Group'),
            (GROUP_CHANGE_PERM, 'Can change a Group'),
            (GROUP_DELETE_PERM, 'Can delete a Group'),
            (GROUP_VIEW_PERM, 'Can view Group'),
            (VOUCHER_VIEW_PERM, 'Can view Voucher'),
            (VOUCHER_DELETE_PERM, 'Can delete Voucher'),
            (VOUCHER_CHANGE_PERM, 'Can change Voucher'),
            (VOUCHER_ADD_PERM, 'Can create Voucher'),
            (TOKEN_GENERATE_PERM, 'Can generate Token'),
            (VOUCHER_ACTIVATE_PERM, 'Can activate Voucher'),
            (VOUCHER_RECHARGE_ACCOUNT_PERM, 'Can recharge an Account')

        ]