from dashboard import Constants



class PermissionManager :
    """
    This Class provides a central to check for permission.
    """

    @staticmethod
    def user_has_perm(user=None, perm=None):
        flag = False
        if user and perm and hasattr(user, 'has_perm'):
            flag = user.has_perm(Constants.APP_PREFIX + perm)
        return flag


    @staticmethod
    def user_can_generate_token(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TOKEN_GENERATE_PERM)

    @staticmethod
    def user_can_access_dashboard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.DASHBOARD_VIEW_PERM)

    @staticmethod
    def user_can_view_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_VIEW_PERM)
    
    @staticmethod
    def user_can_change_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_CHANGE_PERM)

    @staticmethod
    def user_can_add_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_ADD_PERM)
    
    @staticmethod
    def user_can_delete_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_DELETE_PERM)

    ## ACCOUNT PERMISSION
    @staticmethod
    def user_can_view_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_VIEW_PERM)
    
    @staticmethod
    def user_can_change_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_CHANGE_PERM)

    @staticmethod
    def user_can_add_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_ADD_PERM)
    
    @staticmethod
    def user_can_delete_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_DELETE_PERM)
    
    ## GROUP PERMISSION
    @staticmethod
    def user_can_view_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_VIEW_PERM)
    
    @staticmethod
    def user_can_change_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_CHANGE_PERM)

    @staticmethod
    def user_can_add_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_ADD_PERM)
    
    @staticmethod
    def user_can_delete_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_DELETE_PERM)

    ## POLICY PERMISSION
    @staticmethod
    def user_can_view_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_VIEW_PERM)
    
    @staticmethod
    def user_can_change_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_CHANGE_PERM)

    @staticmethod
    def user_can_add_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_ADD_PERM)

    @staticmethod
    def user_can_delete_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_DELETE_PERM)

    ## AVAILABLE SERVICE PERMISSION

    @staticmethod
    def user_can_change_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.AVAILABLE_SERVICE_CHANGE_PERM)

    @staticmethod
    def user_can_view_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.AVAILABLE_SERVICE_VIEW_PERM)

    @staticmethod
    def user_can_add_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.AVAILABLE_SERVICE_ADD_PERM)

    @staticmethod
    def user_can_delete_available_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.AVAILABLE_SERVICE_DELETE_PERM)

    ## SERVICE PERMISSION
    @staticmethod
    def user_can_change_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.SERVICE_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.SERVICE_ADD_PERM)
    
    @staticmethod
    def user_can_delete_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.SERVICE_DELETE_PERM)

    @staticmethod
    def user_can_view_service(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.SERVICE_VIEW_PERM)

    
    ## PAYMENT PERMISSION

    @staticmethod
    def user_can_change_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.PAYMENT_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.PAYMENT_ADD_PERM)
    
    @staticmethod
    def user_can_delete_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.PAYMENT_DELETE_PERM)

    @staticmethod
    def user_can_view_payment(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.PAYMENT_VIEW_PERM)

    
    ## CATEGORY PERMISSION

    @staticmethod
    def user_can_change_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_ADD_PERM)
    
    @staticmethod
    def user_can_delete_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_DELETE_PERM)

    @staticmethod
    def user_can_view_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_VIEW_PERM)

    ## TRANSFER PERMISSION

    @staticmethod
    def user_can_change_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TRANSFER_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TRANSFER_ADD_PERM)
    
    @staticmethod
    def user_can_delete_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TRANSFER_DELETE_PERM)

    @staticmethod
    def user_can_view_transfer(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TRANSFER_VIEW_PERM)

    
    ## VOUCHER PERMISSION

    @staticmethod
    def user_can_change_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.VOUCHER_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.VOUCHER_ADD_PERM)
    
    @staticmethod
    def user_can_delete_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.VOUCHER_DELETE_PERM)

    @staticmethod
    def user_can_view_voucher(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.VOUCHER_VIEW_PERM)

    
    ## IDCARD PERMISSION

    @staticmethod
    def user_can_change_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.IDCARD_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.IDCARD_ADD_PERM)
    
    @staticmethod
    def user_can_delete_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.IDCARD_DELETE_PERM)

    @staticmethod
    def user_can_view_idcard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.IDCARD_VIEW_PERM)

    ## CLAIM PERMISSION

    @staticmethod
    def user_can_change_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CASE_ISSUE_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CASE_ISSUE_ADD_PERM)
    
    @staticmethod
    def user_can_delete_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CASE_ISSUE_DELETE_PERM)

    @staticmethod
    def user_can_view_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CASE_ISSUE_VIEW_PERM)
    
    @staticmethod
    def user_can_close_claim(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CASE_ISSUE_CLOSE_PERM)
    

def get_view_permissions(user=None):
    context = {
        'can_access_dashboard' : PermissionManager.user_can_access_dashboard(user),
        'can_view_available_service': PermissionManager.user_can_view_available_service(user),
        'can_view_service': PermissionManager.user_can_view_service(user),
        'can_view_user': PermissionManager.user_can_view_user(user),
        'can_view_category': PermissionManager.user_can_view_category(user),
        'can_view_group' : PermissionManager.user_can_view_group(user),
        'can_view_policy': PermissionManager.user_can_view_policy(user),
        'can_view_transfer': PermissionManager.user_can_view_transfer(user),
        'can_view_payment': PermissionManager.user_can_view_payment(user),
        'can_view_voucher': PermissionManager.user_can_view_voucher(user),
        'can_add_group' : PermissionManager.user_can_add_group(user),
        'can_generate_token': PermissionManager.user_can_generate_token(user)
    }
    return context