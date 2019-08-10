from django import forms
from accounts.models import Account, Service,Policy, AvailableService,ServiceCategory, IDCard



class PolicyForm(forms.ModelForm):
    
    class Meta:
        model = Policy
        fields = ("daily_limit","weekly_limit", "monthly_limit", "commission",)


class ServiceCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ServiceCategory
        fields = ("category_name", "category_code", "is_active",)



class AvailableServiceForm(forms.ModelForm):
    
    class Meta:
        model = AvailableService
        fields = ("service_code", "name", "operator", "category", "is_active", "description",)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (  'name', 'operator', 'customer', 'customer_reference', 
                    'reference_number', 'category', 'service_instance',
                    'price', 'description', 'issued_at', 'commission',)

class IDCardForm(forms.ModelForm):
    
    class Meta:
        model = IDCard
        fields = ("user","card_number", "is_valid","delivery_at","expire_at","delivery_place",)




class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fileds = ("user","date_of_birth","country",
                  "city","province","address","zip_code","telefon",
                  "newsletter","is_active_account","solde","account_type",
                  "policy","email_validated", )
        