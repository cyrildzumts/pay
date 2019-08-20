from django import forms
from accounts.models import Account, Service,Policy, AvailableService,ServiceCategory, IDCard

class PolicyCreationForm(forms.ModelForm):
    
    class Meta:
        model = Policy
        fields = ("daily_limit","weekly_limit", "monthly_limit", "commission",)
    
    def clean_commission(self):
        commission = self.cleaned_data['commission']
        try:
            policy = Policy.objects.get(commission=commission)
            msg = "A Policy %s entry with commission %s already exists".format(
                policy, commission
            )
            raise forms.ValidationError(msg)
        except Policy.DoesNotExist:
            pass

        return commission

class PolicyForm(forms.ModelForm):
    
    class Meta:
        model = Policy
        fields = ("daily_limit","weekly_limit", "monthly_limit", "commission",)



class ServiceCategoryCreationForm(forms.ModelForm):
    
    class Meta:
        model = ServiceCategory
        fields = ("category_name", "category_code", "is_active",)
        
    def clean_category_name(self):
        name = self.cleaned_data['category_name']
        try:
            category = ServiceCategory.objects.get(category_name=name)
            msg = "A Category with the given name %s already exists".format(
                name
            )
            raise forms.ValidationError(msg)
        except ServiceCategory.DoesNotExist:
            pass
        return name

    def clean_category_code(self):
        code = self.cleaned_data['category_code']
        try:
            category = ServiceCategory.objects.get(category_code=code)
            msg = "A Category with the given name %s already exists".format(
                code
            )
            raise forms.ValidationError(msg)
        except ServiceCategory.DoesNotExist:
            pass
        return code

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
    
    def clean_operator(self):
        operator = self.cleaned_data['operator']
        try:
            Account.objects.get(user=operator)
        except Account.DoesNotExist:
            msg = "There is no Account for the operator %s.".format(
                operator
            )
            raise forms.ValidationError(msg)

        return operator

class IDCardForm(forms.ModelForm):
    
    class Meta:
        model = IDCard
        fields = ("user","card_number", "is_valid","delivery_at","expire_at","delivery_place",)




class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("user","date_of_birth","country",
                  "city","province","address","zip_code","telefon",
                  "newsletter","is_active_account","solde","account_type",
                  "policy","email_validated", )
        