from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from payments.forms import (
    PaymentForm, PolicyForm, ServiceCategoryCreationForm, ServiceCreationForm, AvailableServiceCreationForm,
    TransferForm, CaseIssueForm
)
from payments.tests import policy_test_data, category_test_data, user_test_data, available_service_test_data




class PolicyFormTest(TestCase):
    
    def test_cannot_save_policy_no_daily_limit(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_NO_DAILY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_no_weelky_limit(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_NO_WEEKLY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_no_monthly_limit(self):
        form = PolicyForm(policy_test_data.POLICY_DATA__NO_MONTHLY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_no_commission(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_NO_COMMISSION)
        self.assertFalse(form.is_valid())


    def test_cannot_save_policy_daily_str(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_STR_DAILY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_weekly_str(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_STR_WEEKLY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_monthly_str(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_STR_MONTHLY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_commission_str(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_STR_COMMISSION)
        self.assertFalse(form.is_valid())

    def test_can_save_policy(self):
        form = PolicyForm(policy_test_data.POLICY_DATA)
        self.assertTrue(form.is_valid())


class CategoryFormTest(TestCase):

    def test_cannot_save_category_no_name(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_NAME)
        self.assertFalse(form.is_valid())

    def test_cannot_save_category_no_code(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_CODE)
        self.assertFalse(form.is_valid())

    def test_can_save_category_no_active(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_ACTIVE)
        self.assertTrue(form.is_valid())

    def test_can_save_category(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_ACTIVE)
        self.assertTrue(form.is_valid())

    def test_cannot_save_category_duplicate(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_ACTIVE)
        self.assertTrue(form.is_valid())
        category = form.save()
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_ACTIVE)
        # duplicate is now allowed.
        # unique field is category name
        self.assertFalse(form.is_valid()) 


class AvailableServiceFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.operator = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.category = ServiceCategoryCreationForm.Meta.model.objects.create(**category_test_data.CATEGORY_DATA_NO_ACTIVE)
        self.AVAILABLE_SERVICE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_INITIAL
        self.anonymeUser = AnonymousUser()

    def test_cannot_save_available_service_no_operator_no_category(self):
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # operator entry is set to None
    def test_cannot_save_available_service_no_operator(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # category entry is set to None
    def test_cannot_save_available_service_no_category(self):
        self.AVAILABLE_SERVICE_DATA['operator'] = self.operator.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # operator entry is missing. That is, there is no operator entry at all
    def test_cannot_save_available_service_missing_operator(self):
        self.AVAILABLE_SERVICE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_MISSING_OPERATOR
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # category entry is missing. That is, there is no category entry at all
    def test_cannot_save_available_service_missing_category(self):
        self.AVAILABLE_SERVICE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_MISSING_CATEGORY
        self.AVAILABLE_SERVICE_DATA['operator'] = self.operator.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # anonymeUser pk is allways None. So this test the same no operator test
    def test_cannot_save_available_service_anonyme_operator(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        self.AVAILABLE_SERVICE_DATA['operator'] = self.anonymeUser.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_available_service_not_found_operator(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        self.AVAILABLE_SERVICE_DATA['operator'] = user_test_data.USER_NOT_FOUND_PK
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_available_service_not_found_category(self):
        self.AVAILABLE_SERVICE_DATA['category'] = category_test_data.CATEGORY_NOT_FOUND_PK
        self.AVAILABLE_SERVICE_DATA['operator'] = self.operator.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    
    def test_can_save_available_service(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        self.AVAILABLE_SERVICE_DATA['operator'] = self.operator.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertTrue(form.is_valid())

    
