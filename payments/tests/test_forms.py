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

import logging

logger = logging.getLogger(__name__)



class PolicyFormTest(TestCase):
    
    def test_cannot_save_policy_daily_limit_none(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_NO_DAILY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_weelky_limit_none(self):
        form = PolicyForm(policy_test_data.POLICY_DATA_NO_WEEKLY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_monthly_limit_none(self):
        form = PolicyForm(policy_test_data.POLICY_DATA__NO_MONTHLY)
        self.assertFalse(form.is_valid())

    def test_cannot_save_policy_commission_none(self):
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

    def test_cannot_save_category_name_none(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_NAME)
        self.assertFalse(form.is_valid())

    def test_cannot_save_category_code_none(self):
        form = ServiceCategoryCreationForm(category_test_data.CATEGORY_DATA_NO_CODE)
        self.assertFalse(form.is_valid())

    def test_can_save_category_active_none(self):
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
        self.AVAILABLE_SERVICE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_INITIAL.copy()
        self.anonymeUser = AnonymousUser()

    def test_cannot_save_available_service_operator_and_category_none(self):
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # operator entry is set to None
    def test_cannot_save_available_service_operator_none(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # category entry is set to None
    def test_cannot_save_available_service_category_none(self):
        self.AVAILABLE_SERVICE_DATA['operator'] = self.operator.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # operator entry is missing. That is, there is no operator entry at all
    def test_cannot_save_available_service_operator_missing(self):
        self.AVAILABLE_SERVICE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_MISSING_OPERATOR
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # category entry is missing. That is, there is no category entry at all
    def test_cannot_save_available_service_category_missing(self):
        self.AVAILABLE_SERVICE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_MISSING_CATEGORY
        self.AVAILABLE_SERVICE_DATA['operator'] = self.operator.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    # anonymeUser pk is allways None. So this test the same no operator test
    def test_cannot_save_available_service_operator_anonyme(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        self.AVAILABLE_SERVICE_DATA['operator'] = self.anonymeUser.pk
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_available_service_operator_not_found(self):
        self.AVAILABLE_SERVICE_DATA['category'] = self.category.pk
        self.AVAILABLE_SERVICE_DATA['operator'] = user_test_data.USER_NOT_FOUND_PK
        form = AvailableServiceCreationForm(self.AVAILABLE_SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_available_service_category_not_found(self):
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
        self.inactive_user = User.objects.create_user(**user_test_data.USER_INACTIVE)
        self.anonymeUser = AnonymousUser()

    def test_cannot_save_amount_none(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_NO_AMOUNT
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_amount_missing(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_AMOUNT
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_sender_none(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_none(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_NO_AMOUNT
        PAYMENT_DATA['sender'] = self.sender.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_sender_missing(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_SENDER
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_missing(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_RECIPIENT
        PAYMENT_DATA['sender'] = self.sender.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_detail_missing(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_MISSING_DETAIL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_detail_none(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_NO_DETAIL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_sender_not_found(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = user_test_data.USER_NOT_FOUND_PK
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_not_found(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = user_test_data.USER_NOT_FOUND_PK
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_sender_inactive(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = self.inactive_user.pk
        PAYMENT_DATA['recipient'] = self.recipient.pk
        form = PaymentForm(PAYMENT_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_inactive(self):
        PAYMENT_DATA = payments_test_data.PAYMENT_DATA_INITIAL
        PAYMENT_DATA['sender'] = self.sender.pk
        PAYMENT_DATA['recipient'] = self.inactive_user.pk
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
        self.inactive_user = User.objects.create_user(**user_test_data.USER_INACTIVE)

    def test_cannot_save_amount_none(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_NO_AMOUNT
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_amount_missing(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_AMOUNT
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_sender_none(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_none(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_NO_AMOUNT
        TRANSFER_DATA['sender'] = self.sender.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_sender_missing(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_SENDER
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_missing(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_RECIPIENT
        TRANSFER_DATA['sender'] = self.sender.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())
    
    def test_cannot_save_detail_missing(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_MISSING_DETAIL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_detail_none(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_NO_DETAIL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_sender_not_found(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = user_test_data.USER_NOT_FOUND_PK
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_not_found(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = user_test_data.USER_NOT_FOUND_PK
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_sender_inactive(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = self.inactive_user.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_recipient_inactive(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.inactive_user.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertFalse(form.is_valid())

    def test_can_save(self):
        TRANSFER_DATA = transfer_test_data.TRANSFER_DATA_INITIAL
        TRANSFER_DATA['sender'] = self.sender.pk
        TRANSFER_DATA['recipient'] = self.recipient.pk
        form = TransferForm(TRANSFER_DATA)
        self.assertTrue(form.is_valid())


class ServiceFormTest(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(username=user_test_data.USER_TEST1['username'], email=user_test_data.USER_TEST1['email'], password=user_test_data.USER_TEST1['password'])
        self.operator = User.objects.create_user(username=user_test_data.USER_TEST2['username'], email=user_test_data.USER_TEST2['email'], password=user_test_data.USER_TEST2['password'])
        self.dummy_user = User.objects.create_user(username=user_test_data.USER_TEST3['username'], email=user_test_data.USER_TEST3['email'], password=user_test_data.USER_TEST3['password'])
        self.inactive_user = User.objects.create_user(**user_test_data.USER_INACTIVE)
        self.anonymeUser = AnonymousUser()
        self.category = ServiceCategoryCreationForm.Meta.model.objects.create(**category_test_data.CATEGORY_DATA_NO_ACTIVE)
        AVAILABLE_DATA = available_service_test_data.AVAILABLE_SERVICE_DATA_INITIAL.copy()
        AVAILABLE_DATA['category'] = self.category
        AVAILABLE_DATA['operator'] = self.operator
        self.availabe_service = AvailableServiceCreationForm.Meta.model.objects.create(**AVAILABLE_DATA)
        AVAILABLE_DATA['is_active'] = False
        self.inactive_avs = AvailableServiceCreationForm.Meta.model.objects.create(**AVAILABLE_DATA)
    
    def test_cannot_save_initial_data(self):
        form = ServiceCreationForm(service_test_data.SERVICE_DATA_INITIAL)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_operator(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_not_found_operator(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = user_test_data.USER_NOT_FOUND_PK
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_category(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_not_found_category(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['category'] = category_test_data.CATEGORY_NOT_FOUND_PK
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_no_service_instance(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_issued_at(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['issued_at'] = service_test_data.SERVICE_ISSUED_AT_BAD
        logger.info("Service Test BAD DATE : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad2_issued_at(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['issued_at'] = service_test_data.SERVICE_ISSUED_AT_BAD_DD_MM_YYYY
        logger.info("Service Test BAD_2 DD_MM_YYYY DATE : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad3_issued_at(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['issued_at'] = service_test_data.SERVICE_ISSUED_AT_BAD_MM_DD_YYYY
        logger.info("Service Test BAD_3 MM_DD_YYYY DATE : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_commission(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION_BAD
        logger.info("Service Test BAD COMMISSION : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_2_commission(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION_BAD_2
        logger.info("Service Test BAD_2 COMMISSION : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_bad_3_commission(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION_BAD_3
        logger.info("Service Test BAD_3 COMMISSION : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        self.assertFalse(form.is_valid())

    def test_cannot_save_operator_is_not_available_service_operator(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.dummy_user.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        logger.info("Service Test OPERATOR_NOT_AVS_OPERATOR : %s", SERVICE_DATA)
        form = ServiceCreationForm(SERVICE_DATA)
        is_valid = form.is_valid()
        """
        if not is_valid:
            logger.error("ServiceCreationForm is not valid.")            
            for field in form:
                logger.error("\t\tServiceCreationForm Field %s", field)
                if field.errors:
                    for e in field.errors:
                        logger.error("\t\t\tServiceCreationForm Error  : %s: ", e)
        """
        self.assertFalse(is_valid)

    
    def test_cannot_save_inactive_operator(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.inactive_user.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION
        logger.info("Service Test CAN SAVE : %s", SERVICE_DATA)

        form = ServiceCreationForm(SERVICE_DATA)

        is_valid = form.is_valid()
        """
        if not is_valid:
            logger.error("ServiceCreationForm is not valid.")            
            for field in form:
                logger.error("\t\tServiceCreationForm Field %s", field)
                if field.errors:
                    for e in field.errors:
                        logger.error("\t\t\tServiceCreationForm Error  : %s: ", e)

        """
        self.assertFalse(is_valid)
    
    def test_cannot_save_inactive_customer(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.inactive_user.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION
        logger.info("Service Test CAN SAVE : %s", SERVICE_DATA)

        form = ServiceCreationForm(SERVICE_DATA)

        is_valid = form.is_valid()
        """
        if not is_valid:
            logger.error("ServiceCreationForm is not valid.")            
            for field in form:
                logger.error("\t\tServiceCreationForm Field %s", field)
                if field.errors:
                    for e in field.errors:
                        logger.error("\t\t\tServiceCreationForm Error  : %s: ", e)

        """
        self.assertFalse(is_valid)
    
    def test_cannot_save_inactive_available_service(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.inactive_user.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.inactive_avs.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION
        logger.info("Service Test CAN SAVE : %s", SERVICE_DATA)

        form = ServiceCreationForm(SERVICE_DATA)

        is_valid = form.is_valid()
        """
        if not is_valid:
            logger.error("ServiceCreationForm is not valid.")            
            for field in form:
                logger.error("\t\tServiceCreationForm Field %s", field)
                if field.errors:
                    for e in field.errors:
                        logger.error("\t\t\tServiceCreationForm Error  : %s: ", e)

        """
        self.assertFalse(is_valid)


    def test_can_save(self):
        SERVICE_DATA = service_test_data.SERVICE_DATA_INITIAL.copy()
        SERVICE_DATA['operator'] = self.operator.pk
        SERVICE_DATA['customer'] = self.customer.pk
        SERVICE_DATA['category'] = self.category.pk
        SERVICE_DATA['service_instance'] = self.availabe_service.pk
        SERVICE_DATA['commission'] = service_test_data.SERVICE_COMMISSION
        logger.info("Service Test CAN SAVE : %s", SERVICE_DATA)

        form = ServiceCreationForm(SERVICE_DATA)

        is_valid = form.is_valid()
        """
        if not is_valid:
            logger.error("ServiceCreationForm is not valid.")            
            for field in form:
                logger.error("\t\tServiceCreationForm Field %s", field)
                if field.errors:
                    for e in field.errors:
                        logger.error("\t\t\tServiceCreationForm Error  : %s: ", e)

        """
        self.assertTrue(is_valid)

