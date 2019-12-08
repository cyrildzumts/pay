from django.db import models

# Create your models here.
class AccessPermissions(models.Model):
    DASHBOARD_VIEW_PERM                 = 'can_view_dashboard'

    ACCOUNT_VIEW_PERM                     = 'can_view_account'
    ACCOUNT_CREATE_PERM                   = 'can_add_account'
    ACCOUNT_CHANGE_PERM                   = 'can_change_account'
    ACCOUNT_DELETE_PERM                   = 'can_delete_account'

    CASE_ISSUE_VIEW_PERM                     = 'can_view_claim'
    CASE_ISSUE_CREATE_PERM                   = 'can_add_claim'
    CASE_ISSUE_CHANGE_PERM                   = 'can_change_claim'
    CASE_ISSUE_DELETE_PERM                   = 'can_delete_claim'
    CASE_ISSUE_CLOSE_PERM                    = 'can_close_claim'

    GROUP_VIEW_PERM                     = 'can_view_group'
    GROUP_CREATE_PERM                   = 'can_add_group'
    GROUP_CHANGE_PERM                   = 'can_change_group'
    GROUP_DELETE_PERM                   = 'can_delete_group'

    IDCARD_VIEW_PERM                    = 'can_view_idcard'
    IDCARD_CREATE_PERM                  = 'can_add_idcard'
    IDCARD_CHANGE_PERM                  = 'can_change_idcard'
    IDCARD_DELETE_PERM                  = 'can_delete_idcard'

    VOUCHER_VIEW_PERM                   = 'can_view_voucher'
    VOUCHER_CREATE_PERM                 = 'can_add_voucher'
    VOUCHER_CHANGE_PERM                 = 'can_change_voucher'
    VOUCHER_DELETE_PERM                 = 'can_delete_voucher'
    VOUCHER_ACTIVATE_PERM               = 'can_activate_voucher'
    VOUCHER_RECHARGE_ACCOUNT_PERM       = 'can_recharge_account_voucher'

    PAYMENT_VIEW_PERM                   = 'can_view_payment'
    PAYMENT_CREATE_PERM                 = 'can_add_payment'
    PAYMENT_CHANGE_PERM                 = 'can_change_payment'
    PAYMENT_DELETE_PERM                 = 'can_delete_payment'

    POLICY_VIEW_PERM                    = 'can_view_policy'
    POLICY_CREATE_PERM                  = 'can_add_policy'
    POLICY_CHANGE_PERM                  = 'can_change_policy'
    POLICY_DELETE_PERM                  = 'can_delete_policy'

    CATEGORY_VIEW_PERM                  = 'can_view_category'
    CATEGORY_CREATE_PERM                = 'can_add_category'
    CATEGORY_CHANGE_PERM                = 'can_change_category'
    CATEGORY_DELETE_PERM                = 'can_delete_category'

    AVAILABLE_SERVICE_VIEW_PERM         = 'can_view_available_service'
    AVAILABLE_SERVICE_CREATE_PERM       = 'can_add_available_service'
    AVAILABLE_SERVICE_CHANGE_PERM       = 'can_change_available_service'
    AVAILABLE_SERVICE_DELETE_PERM       = 'can_delete_available_service'

    SERVICE_VIEW_PERM                   = 'can_view_service'
    SERVICE_CREATE_PERM                 = 'can_add_service'
    SERVICE_CHANGE_PERM                 = 'can_change_service'
    SERVICE_DELETE_PERM                 = 'can_delete_service'

    TRANSFER_VIEW_PERM                  = 'can_view_transfer'
    TRANSFER_CREATE_PERM                = 'can_add_transfer'
    TRANSFER_CHANGE_PERM                = 'can_change_transfer'
    TRANSFER_DELETE_PERM                = 'can_delete_transfer'

    REDUCTION_VIEW_PERM                  = 'can_view_reduction'
    REDUCTION_CREATE_PERM                = 'can_add_reduction'
    REDUCTION_CHANGE_PERM                = 'can_change_reduction'
    REDUCTION_DELETE_PERM                = 'can_delete_reduction'


    class Meta:
        managed = False
        permissions = {
            ('can_view_dashboard', 'Can view Dashboard'),
            ('can_add_group', 'Can create a Group'),
            ('can_change_group', 'Can change a Group'),
            ('can_delete_group', 'Can delete a Group'),
            ('can_view_voucher', 'Can view Voucher'),
            ('can_delete_voucher', 'Can delete Voucher'),
            ('can_change_voucher', 'Can change Voucher'),
            ('can_add_voucher', 'Can create Voucher'),
            ('can_activate_voucher', 'Can activate Voucher'),
            ('can_recharge_account', 'Can recharge an Account'),

        }