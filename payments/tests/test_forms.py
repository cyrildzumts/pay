from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from payments.forms import (
    PaymentForm, PolicyForm, ServiceCategoryCreationForm, ServiceCreationForm, AvailableServiceCreationForm,
    TransferForm, CaseIssueForm
)
from payments.tests import (
    policy_test_data, category_test_data, user_test_data, available_service_test_data, payments_test_data, transfer_test_data,
    service_test_data

)




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

    
class PaymentFormTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.recipient = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.anonymeUser = AnonymousUser()

    def test_cannot_save_no_amount(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_NO_AMOUNT
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_missing_amount(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_AMOUNT
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_no_sender(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_recipient(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_NO_AMOUNT
        PAYMENT_DATA['sender'] = self.sender.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_missing_sender(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_SENDER
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_missing_recipient(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_RECIPIENT
        PAYMENT_DATA['sender'] = self.sender.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_missing_detail(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_DETAIL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_detail(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_NO_DETAIL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_not_found_sender(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = user_test_data.USER_NOT_FOUND_PK
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_not_found_recipient(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = user_test_data.USER_NOT_FOUND_PK
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_can_save(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertTrue(form.is_valid())


class TransferFormTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.recipient = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.anonymeUser = AnonymousUser()

    def test_cannot_save_no_amount(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_NO_AMOUNT
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_missing_amount(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_AMOUNT
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_no_sender(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_recipient(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_NO_AMOUNT
        TRANSFER_DATA['sender'] = self.sender.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_missing_sender(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_SENDER
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_missing_recipient(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_RECIPIENT
        TRANSFER_DATA['sender'] = self.sender.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_missing_detail(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_DETAIL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_detail(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_NO_DETAIL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_not_found_sender(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = user_test_data.USER_NOT_FOUND_PK
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_not_found_recipient(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = user_test_data.USER_NOT_FOUND_PK
        form = PaymentForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_can_save(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(TRANSFER_DATA)
        self.assertTrue(form.is_valid())



class ServiceFormTest(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.operator = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.dummy_user = User.objects.create_user(username=user_test_data.USER_TEST3['username'], email=user_test_data.USER_TEST3['email'], password=user_test_data.USER_TEST3['password'])
        self.anonymeUser = AnonymousUser()
        self.category = ServiceCategoryCreationForm.Meta.model.objects.create(**category_test_data.CATEGORY_DATA_NO_ACTIVE)
        AVAILABLE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_INITIAL
        AVAILABLE_DATA['category'] = self.category
        AVAILABLE_DATA['operator'] = self.operator
        self.availabe_service = AvailableServiceCreationForm.Meta.model.objects.create(**AVAILABLE_DATA)
    
    def test_cannot_save_initial_data(self):
        form = ServiceCreationForm(service_test_data.SERVICE_DATA_INITIAL)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_operator(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_category(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_service_instance(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_issued_at(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['issued_at'] = service_test_data.SERVICE_ISSUED_AT_BAD
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad2_issued_at(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['issued_at'] = service_test_data.SERVICE_ISSUED_AT_BAD_DD_MM_YYYY
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad3_issued_at(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['issued_at'] = service_test_data.SERVICE_ISSUED_AT_BAD_MM_DD_YYYY
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_commission(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION_BAD
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_2_commission(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION_BAD_2
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_3_commission(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION_BAD_3
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_operator_is_not_available_service_operator(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL
        SERVICE_DATA['operator'] = self.dummy_user.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())