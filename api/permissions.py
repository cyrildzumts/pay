from rest_framework import permissions as rest_perms

class CanReadVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        flag = False
        if request.user.is_authenticated:
            flag = request.user.has_permission('api_view_voucher')
        return flag
    

    def has_object_permission(self, request, view, obj):
        return False


class CanChangeVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        flag = False
        if request.user.is_authenticated:
            flag = request.user.has_permission('api_change_voucher')
        return flag
    

    def has_object_permission(self, request, view, obj):
        return False


class CanDeleteVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        flag = False
        if request.user.is_authenticated:
            flag = request.user.has_permission('api_delete_voucher')
        return flag
    

    def has_object_permission(self, request, view, obj):
        return False
    

class CanAddVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        flag = False
        if request.user.is_authenticated:
            flag = request.user.has_permission('api_add_voucher')
        return flag
    

    def has_object_permission(self, request, view, obj):
        return False