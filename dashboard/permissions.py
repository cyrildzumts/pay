from dashboard.models import AccessPermissions



class PermissionManager :
    """
    This Class provides a central to check for permission.
    """

    @staticmethod
    def user_has_perm(user=None, perm=None):
        flag = False
        if user and perm and hasattr(user, 'has_perm'):
            flag = user.has_perm(perm)
        return flag


    @staticmethod
    def user_can_access_dashboard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.DASHBOARD_VIEW_PERM)

    ## ACCOUNT PERMISSION
    @staticmethod
    def user_can_view_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.ACCOUNT_VIEW_PERM)
    
    @staticmethod
    def user_can_change_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.ACCOUNT_CHANGE_PERM)

    @staticmethod
    def user_can_add_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.ACCOUNT_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.ACCOUNT_DELETE_PERM)
    
    ## GROUP PERMISSION
    @staticmethod
    def user_can_view_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.GROUP_VIEW_PERM)
    
    @staticmethod
    def user_can_change_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.GROUP_CHANGE_PERM)

    @staticmethod
    def user_can_add_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.GROUP_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.GROUP_DELETE_PERM)

    ## POLICY PERMISSION
    @staticmethod
    def user_can_view_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.POLICY_VIEW_PERM)
    
    @staticmethod
    def user_can_change_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.POLICY_CHANGE_PERM)

    @staticmethod
    def user_can_add_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.POLICY_CREATE_PERM)

    @staticmethod
    def user_can_delete_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.POLICY_DELETE_PERM)

    ## AVAILABLE SERVICE PERMISSION

    @staticmethod
    def user_can_change_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.AVAILABLE_SERVICE_CHANGE_PERM)

    @staticmethod
    def user_can_view_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.AVAILABLE_SERVICE_VIEW_PERM)

    @staticmethod
    def user_can_add_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.AVAILABLE_SERVICE_CREATE_PERM)

    @staticmethod
    def user_can_delete_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.AVAILABLE_SERVICE_DELETE_PERM)

    ## SERVICE PERMISSION
    @staticmethod
    def user_can_change_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.SERVICE_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.SERVICE_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.SERVICE_DELETE_PERM)

    @staticmethod
    def user_can_view_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.SERVICE_VIEW_PERM)

    
    ## PAYMENT PERMISSION

    @staticmethod
    def user_can_change_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.PAYMENT_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.PAYMENT_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.PAYMENT_DELETE_PERM)

    @staticmethod
    def user_can_view_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.PAYMENT_VIEW_PERM)

    
    ## CATEGORY PERMISSION

    @staticmethod
    def user_can_change_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CATEGORY_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CATEGORY_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CATEGORY_DELETE_PERM)

    @staticmethod
    def user_can_view_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CATEGORY_VIEW_PERM)

    ## TRANSFER PERMISSION

    @staticmethod
    def user_can_change_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.TRANSFER_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.TRANSFER_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.TRANSFER_DELETE_PERM)

    @staticmethod
    def user_can_view_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.TRANSFER_VIEW_PERM)

    
    ## VOUCHER PERMISSION

    @staticmethod
    def user_can_change_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.VOUCHER_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.VOUCHER_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.VOUCHER_DELETE_PERM)

    @staticmethod
    def user_can_view_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.VOUCHER_VIEW_PERM)

    
    ## IDCARD PERMISSION

    @staticmethod
    def user_can_change_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.IDCARD_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.IDCARD_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.IDCARD_DELETE_PERM)

    @staticmethod
    def user_can_view_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.IDCARD_VIEW_PERM)

    ## CLAIM PERMISSION

    @staticmethod
    def user_can_change_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CASE_ISSUE_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CASE_ISSUE_CREATE_PERM)
    
    @staticmethod
    def user_can_delete_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CASE_ISSUE_DELETE_PERM)

    @staticmethod
    def user_can_view_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CASE_ISSUE_VIEW_PERM)
    
    @staticmethod
    def user_can_close_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=AccessPermissions.CASE_ISSUE_CLOSE_PERM)