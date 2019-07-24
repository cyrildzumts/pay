from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from voucher.models import Voucher, SoldVoucher, UsedVoucher
# Register your models here.

class VoucherInline(admin.StackedInline):
    model = Voucher

class SoldVoucherInline(admin.StackedInline):
    model = SoldVoucher
    fk_name = 'voucher'


class UsedVoucherInline(admin.StackedInline):
    model = UsedVoucher
    fk_name = 'voucher'



@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    inlines = (VoucherInline, SoldVoucherInline, UsedVoucherInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(VoucherAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User ,VoucherAdmin)
admin.site.register( Voucher)
admin.site.register(SoldVoucher)
admin.site.register(UsedVoucher)
