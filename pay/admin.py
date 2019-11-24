from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from pay.forms import CustomGroupForm



# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = CustomGroupForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)