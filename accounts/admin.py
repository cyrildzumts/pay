from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import  Policy, Account, IDCard

# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'accounts'


class PolicyInline(admin.StackedInline):
    model = Policy
    can_delete = False
    verbose_name_plural = 'policies'


class IDCardInline(admin.StackedInline):
    model = IDCard
    can_delete = False



class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, PolicyInline, IDCardInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)