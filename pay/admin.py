from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from pay.models import  Policy, Account, IDCard, Transaction, CaseIssue, Reduction
from pay.forms import CustomGroupForm



# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = CustomGroupForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']




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


class TransactionInline(admin.StackedInline):
    model  = Transaction
    can_delete = False


class ReductionInline(admin.StackedInline):
    model = Reduction
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, PolicyInline,
    IDCardInline,TransactionInline, ReductionInline)

    

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)