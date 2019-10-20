from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import  Policy, Account, IDCard, Service, ServiceCategory, AvailableService

# Register your models here.

class ServiceInline(admin.StackedInline):
    model = Service
    can_delete = False
    verbose_name_plural = 'Services'

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    fk_name = 'user'
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



class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountInline, IDCardInline]
    list_display = ['user', 'country', 'city', 'telefon', 'created_by', 'solde']
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AccountAdmin, self).get_inline_instances(request, obj)



admin.site.unregister(User)
admin.site.register(User ,AccountAdmin)
admin.site.register(Account)
admin.site.register( Policy)
admin.site.register(ServiceCategory)
admin.site.register(AvailableService)
admin.site.register(Service)
admin.site.register(IDCard)