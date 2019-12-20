from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from payments.forms import (
    PaymentForm, PolicyForm, ServiceCategoryCreationForm, ServiceCreationForm, AvailableServiceCreationForm,
    TransferForm, CaseIssueForm
)
from payments.tests import policy_test_data, category_test_data




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