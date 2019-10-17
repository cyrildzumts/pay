from rest_framework import permissions as rest_perms

class CanReadVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_permission('api_view_voucher')
    

    def has_object_permission(self, request, view, obj):
        return False


class CanChangeVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_permission('api_change_voucher')
    

    def has_object_permission(self, request, view, obj):
        return False


class CanDeleteVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_permission('api_delete_voucher')
    

    def has_object_permission(self, request, view, obj):
        return False
    

class CanAddVoucherPermission(rest_perms.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_permission('api_add_voucher')
    

    def has_object_permission(self, request, view, obj):
        return False