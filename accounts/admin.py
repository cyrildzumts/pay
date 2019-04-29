from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import  Policy, Account, IDCard

# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Profile'

'''
class PolicyInline(admin.StackedInline):
    model = Policy
    can_delete = False
    verbose_name_plural = 'policies'
'''

class IDCardInline(admin.StackedInline):
    model = IDCard
    can_delete = False



class AccountAdmin(UserAdmin):
    inlines = [AccountInline, IDCardInline,]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AccountAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User ,AccountAdmin)
admin.site.register( Policy)